"""对照冻结 Git tree 验证译文。--partial 只要求已校对文件完成翻译。

运行：rtk proxy uv run --isolated --no-project --with pyyaml --with markdown-it-py
      --with beautifulsoup4 python docs/localization/validate.py [--partial]
不会安装技能、执行示例或修改源仓库。
"""
from pathlib import Path, PurePosixPath
from collections import Counter
from urllib.parse import unquote, urlsplit
from html.parser import HTMLParser
import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import yaml
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = json.loads((ROOT / 'docs/localization/manifest.json').read_text())
REVIEWS = json.loads((ROOT / 'docs/localization/review.json').read_text())
MD = MarkdownIt('commonmark', {'html': True}).enable('table')
ERRORS = []
NOTES = []
BASELINE_LINKS = []
RESIDUALS = []

class Markup(HTMLParser):
    """记录 HTML 标签与属性，并报告不匹配嵌套；普通文本可翻译。"""
    VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self, ignore_ids=()):
        super().__init__(convert_charrefs=True)
        self.events = []
        self.stack = []
        self.problems = []
        self.ignore_ids = set(ignore_ids)
        self.ignored_anchor = False

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and dict(attrs).get('id') in self.ignore_ids and len(attrs) == 1:
            self.ignored_anchor = True
            return
        self.events.append(('open',tag,attrs))
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_startendtag(self,tag,attrs):
        self.events.append(('empty',tag,attrs))

    def handle_endtag(self,tag):
        if tag == 'a' and self.ignored_anchor:
            self.ignored_anchor = False
            return
        self.events.append(('close',tag))
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.problems.append('不匹配关闭标签: '+tag)

    def finish(self,text):
        self.feed(text)
        self.close()
        self.problems.extend('未闭合标签: '+t for t in self.stack)
        return self

def raw_markup(ts):
    chunks = []
    for t in ts:
        if t.type == 'html_block':
            chunks.append(t.content)
        for c in t.children or []:
            if c.type == 'html_inline':
                chunks.append(c.content)
    return '\n'.join(chunks)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(['git', '-C', MANIFEST['source_path'], *args])

def check(condition, message):
    if not condition:
        ERRORS.append(message)

def flatten(value, path='$'):
    result = {path: ('object' if isinstance(value, dict) else 'array' if isinstance(value, list) else type(value).__name__, None if isinstance(value, (dict,list)) else value)}
    if isinstance(value, dict):
        for key, child in value.items():
            result.update(flatten(child, path + '.' + str(key)))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            result.update(flatten(child, path + '[' + str(i) + ']'))
    return result

def compare_metadata(path, source, target, allowed):
    a, b = flatten(source), flatten(target)
    check(a.keys() == b.keys(), path + ': 元数据字段集合变化')
    for key in a.keys() & b.keys():
        check(a[key][0] == b[key][0], path + ': 字段类型变化 ' + key)
        if key not in allowed:
            check(a[key] == b[key], path + ': 不可变元数据变化 ' + key)

def split_frontmatter(text):
    if not text.startswith('---\n'):
        return None, text
    chunks = text.split('\n---\n', 1)
    if len(chunks) != 2:
        raise ValueError('frontmatter 未闭合')
    return yaml.safe_load(chunks[0][4:]), chunks[1]

def tokens(text):
    return MD.parse(split_frontmatter(text)[1])

def links(text):
    result = []
    for token in tokens(text):
        for child in token.children or []:
            if child.type == 'link_open':
                result.append(child.attrGet('href'))
            elif child.type == 'image':
                result.append(child.attrGet('src'))
        if token.type in ['html_block', 'inline']:
            soup = BeautifulSoup(token.content, 'html.parser')
            for element in soup.find_all(['a','img']):
                value = element.get('href') or element.get('src')
                if value:
                    result.append(value)
    return result

def inline_code(text):
    return Counter(c.content for token in tokens(text) for c in token.children or [] if c.type == 'code_inline')

def section_links(text):
    """按标题顺序核对索引分组，防止技能在用户/模型调用组之间移动。"""
    groups = [[]]
    for token in tokens(text):
        if token.type == 'heading_open':
            groups.append([])
        for child in token.children or []:
            if child.type == 'link_open':
                groups[-1].append(child.attrGet('href'))
    return groups

def protected_inline_code(path, source, target):
    original, translated = inline_code(source), inline_code(target)
    for change in MANIFEST.get('inline_code_translations', {}).get(path, []):
        if not original[change['source']] and not translated[change['target']]:
            continue
        check(original[change['source']] == translated[change['target']] > 0,
              path + ': 登记的自然语言内联例句缺失或数量改变')
        translated[change['source']] += translated.pop(change['target'], 0)
    return original == translated

def slug(value):
    value = re.sub(r'<[^>]*>', '', value).lower()
    value = re.sub(r'[^\w\- ]', '', value, flags=re.UNICODE)
    return value.replace(' ', '-')

def anchors(text):
    ids = set(re.findall(r'\bid=["\x27]([^"\x27]+)', text))
    seen = Counter()
    ts = tokens(text)
    for i,t in enumerate(ts):
        if t.type == 'heading_open':
            content = ''.join(c.content for c in (ts[i+1].children or []) if c.type in ['text','code_inline'])
            key = slug(content)
            n = seen[key]
            seen[key] += 1
            ids.add(key + ('-' + str(n) if n else ''))
    return ids

def local_link_result(path, link, contents):
    if link.startswith(('http:', 'https:', 'mailto:', 'data:', 'tel:')):
        return None
    parsed = urlsplit(link)
    target = unquote(parsed.path)
    if re.search(r'[<>*{}]', target) or target.startswith(('~/', '/')):
        return '示例、占位符或使用者项目路径'
    resolved = os.path.normpath(str(PurePosixPath(path).parent / target)) if target else path
    if resolved not in contents:
        if any(p.startswith(resolved.rstrip('/') + '/') for p in contents):
            return None
        return '路径不存在: ' + resolved
    if parsed.fragment and resolved.endswith('.md'):
        if unquote(parsed.fragment) not in anchors(contents[resolved]):
            return '锚点不存在: ' + resolved + '#' + parsed.fragment
    return None

def check_doc(path, source, target):
    if path == 'README.md':
        notice = MANIFEST.get('readme_notice', '')
        if notice:
            check(target.startswith(notice), 'README.md: 中文声明与登记内容不一致')
            target = target.removeprefix(notice)
    for addition in MANIFEST.get('localized_additions', {}).get(path, []):
        check(target.count(addition['text']) == 1, path + ': 登记的本地索引补充缺失或重复')
        check(addition['text'] not in source, path + ': 本地补充已存在于源文件，应重新审查例外')
        target = target.replace(addition['text'], '')
    a, b = tokens(source), tokens(target)
    check([t.tag for t in a if t.type == 'heading_open'] == [t.tag for t in b if t.type == 'heading_open'], path + ': 标题数量或层级变化')
    table_types = {'table_open','thead_open','tbody_open','tr_open','th_open','td_open'}
    check([t.type for t in a if t.type in table_types] == [t.type for t in b if t.type in table_types], path + ': 表格结构变化')
    fa, fb = [t for t in a if t.type == 'fence'], [t for t in b if t.type == 'fence']
    check([t.info for t in fa] == [t.info for t in fb], path + ': fenced block 数量或语言变化')
    record = REVIEWS.get(path, {})
    declared = {f['index']: f['method'] for f in record.get('fences', [])}
    for i,(x,y) in enumerate(zip(fa,fb)):
        if x.content != y.content:
            check(i in declared and declared[i] != '原样代码块', path + ': 未登记的代码块变化 ' + str(i))
            check(protected_inline_code(path, x.content, y.content), path + ': 翻译模板中的内联技术字面量变化 ' + str(i))
            NOTES.append({'path': path, 'fence': i, 'kind': '已登记的自然语言代码块翻译，语义由全文校对记录覆盖'})
        if x.info.strip() == 'html':
            original_html = Markup().finish(x.content)
            target_html = Markup().finish(y.content)
            check(original_html.events == target_html.events, path + ': HTML 代码块标签或属性改变 ' + str(i))
            check(original_html.problems == target_html.problems, path + ': HTML 代码块新增嵌套错误 ' + str(i))
    anchor_file = ROOT / 'docs/localization/anchors.json'
    mapping = json.loads(anchor_file.read_text()) if anchor_file.exists() else {}
    compatible = [e['fragment'] for e in mapping.get(path,[])]
    original_html = Markup().finish(raw_markup(a))
    target_html = Markup(compatible).finish(raw_markup(b))
    # 只允许逐项登记的自然语言属性译文，href/src/id 等仍严格比较。
    for change in MANIFEST.get('html_attribute_translations', {}).get(path, []):
        normalized = []
        for event in target_html.events:
            if event[0] in ['open', 'empty'] and event[1] == change['tag']:
                attrs = [(key, change['source'] if key == change['attribute'] and value == change['target'] else value) for key, value in event[2]]
                event = (event[0], event[1], attrs)
            normalized.append(event)
        target_html.events = normalized
    check(original_html.events == target_html.events, path + ': 正文 HTML 标签或属性改变')
    check(original_html.problems == target_html.problems, path + ': 正文 HTML 新增嵌套问题')
    check(anchors(source) <= anchors(target), path + ': 原标题锚点未完整兼容')
    check(Counter(links(source)) == Counter(links(target)), path + ': 链接或图片目标变化')
    if path == 'README.md' or (path.startswith('skills/') and path.count('/') == 2 and path.endswith('/README.md')):
        check(section_links(source) == section_links(target), path + ': 技能索引次序或调用分组改变')
    check(protected_inline_code(path, source, target), path + ': 内联代码字面量变化，须人工逐项登记')
    # 只扫描普通段落的英文候选；代码块、元数据、固定标题另由校对记录说明。
    for t in b:
        if t.type == 'inline' and re.search(r'[A-Za-z]+(?:[ ,;]+[A-Za-z]+){7,}', t.content) and not re.search(r'[\u4e00-\u9fff]', t.content):
            RESIDUALS.append({'path':path,'text':t.content,'status':'待逐项分类'})

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--partial', action='store_true')
    args = parser.parse_args()
    entries = MANIFEST['entries']
    tree = {}
    for row in git('ls-tree','-rz',MANIFEST['source_commit']).split(b'\0'):
        if row:
            head,path = row.split(b'\t')
            mode,kind,blob = head.decode().split()
            tree[path.decode()] = (mode,blob)
    snapshot_counts = MANIFEST['snapshot_counts']
    check(len(tree) == snapshot_counts['paths'], '冻结树路径数与登记快照不一致')
    check(git('rev-parse', MANIFEST['source_commit'] + '^{tree}').decode().strip() == MANIFEST['source_tree'], '冻结 Git tree 标识不符')
    check(git('rev-parse', 'HEAD').decode().strip() == MANIFEST['source_commit'], '源仓库 HEAD 已离开冻结提交')
    check(set(tree) == {e['path'] for e in entries}, 'manifest 路径集合与冻结树不一致')
    contents = {}
    targets = {}
    for entry in entries:
        path = entry['path']; p = ROOT / path
        check(tree.get(path) == (entry['mode'],entry['source_blob']), path + ': manifest mode/blob 不符')
        raw = git('cat-file','blob',entry['source_blob'])
        check(sha(raw) == entry['source_sha256'], path + ': 源 hash 不符')
        check(p.exists() or p.is_symlink(), path + ': 缺失目标文件')
        if not (p.exists() or p.is_symlink()):
            continue
        if entry['mode'] == '120000':
            check(p.is_symlink() and os.readlink(p) == raw.decode(), path + ': 符号链接不符')
            continue
        check(not p.is_symlink() and p.is_file(), path + ': 文件类型不符')
        check(bool(p.stat().st_mode & 0o111) == (entry['mode'] == '100755'), path + ': 可执行位不符')
        translated = p.read_bytes()
        if entry['method'] == '原样保留':
            check(raw == translated, path + ': 原样文件 bytes 改变')
        if entry.get('validated_target_sha256'):
            check(sha(translated) == entry['validated_target_sha256'], path + ': 最终验收后目标 hash 变化')
        try:
            source, target = raw.decode(), translated.decode()
        except UnicodeDecodeError:
            continue
        contents[path], targets[path] = source, target
        record = REVIEWS.get(path)
        if entry['method'] != '原样保留':
            if not args.partial:
                check(bool(record), path + ': 缺少全文校对记录')
            if record:
                check(record['source_sha256'] == sha(raw), path + ': 校对源 hash 过期')
                check(record['target_sha256'] == sha(translated), path + ': 校对目标 hash 过期')
        try:
            if path.endswith('.json'):
                compare_metadata(path,json.loads(source),json.loads(target),MANIFEST['mutable_json_paths'].get(path,[]))
            elif path.endswith(('.yaml','.yml')):
                allowed = ['$.interface.short_description'] if path.endswith('agents/openai.yaml') else MANIFEST.get('mutable_yaml_paths', {}).get(path, [])
                compare_metadata(path,yaml.safe_load(source),yaml.safe_load(target),allowed)
            elif path.endswith('.md'):
                sm, sb = split_frontmatter(source); tm, tb = split_frontmatter(target)
                allowed = ['$.description','$.argument-hint'] if path.endswith('/SKILL.md') else []
                compare_metadata(path,sm,tm,allowed)
                if record or not args.partial:
                    check_doc(path,source,target)
        except Exception as exc:
            ERRORS.append(path + ': 解析错误 ' + str(exc))
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if (p.is_file() or p.is_symlink()) and '.git' not in p.relative_to(ROOT).parts}
    extra = actual - set(tree)
    check(extra <= set(MANIFEST['additional_path_allowlist']), '未登记额外路径: ' + str(sorted(extra - set(MANIFEST['additional_path_allowlist']))))
    for path,expected in MANIFEST['existing_files'].items():
        check(sha((ROOT/path).read_bytes()) == expected, path + ': 用户既有文件改变')
    wiki = ROOT / 'wiki/translation.html'
    if wiki.exists():
        page = wiki.read_text()
        html_check = Markup().finish(page)
        check(not html_check.problems, 'wiki/translation.html: HTML 嵌套错误 ' + str(html_check.problems))
        soup = BeautifulSoup(page,'html.parser')
        check(bool(soup.html) and soup.html.get('lang') == 'zh-CN', 'wiki/translation.html: 缺少中文语言标记')
        check(any(a.get('href') == '../README.md' for a in soup.find_all('a')), 'wiki/translation.html: 缺少返回 README 链接')
        check('wiki/translation.html' in links(targets['README.md']), 'README 缺少中文说明链接')
        for anchor in soup.find_all('a', href=True):
            url = urlsplit(anchor['href'])
            if not url.scheme and url.path:
                check((wiki.parent / unquote(url.path)).resolve().exists(), 'wiki/translation.html: 本地链接不存在 ' + anchor['href'])
    elif not args.partial:
        check(False, '缺少 wiki/translation.html')
    for path in MANIFEST['additional_path_allowlist']:
        if not path.startswith('wiki/') or not path.endswith('.html') or path in MANIFEST['existing_files']:
            continue
        page_path = ROOT / path
        check(page_path.is_file(), path + ': 缺少已登记的用户说明页')
        if not page_path.is_file():
            continue
        page = page_path.read_text()
        html_check = Markup().finish(page)
        check(not html_check.problems, path + ': HTML 嵌套错误 ' + str(html_check.problems))
        soup = BeautifulSoup(page, 'html.parser')
        check(bool(soup.html) and soup.html.get('lang') == 'zh-CN', path + ': 缺少中文语言标记')
        for anchor in soup.find_all('a', href=True):
            url = urlsplit(anchor['href'])
            if not url.scheme and url.path:
                check((page_path.parent / unquote(url.path)).resolve().exists(), path + ': 本地链接不存在 ' + anchor['href'])
    skill_paths = [p for p in tree if p.endswith('/SKILL.md')]
    check(len(skill_paths) == snapshot_counts['skills'], '技能数量与登记快照不一致')
    check(Counter(p.split('/')[1] for p in skill_paths) == snapshot_counts['buckets'], '分类技能数量不符')
    check(sum(p.endswith('/agents/openai.yaml') for p in tree) == snapshot_counts['agents'], 'agent 元数据数量不符')
    promoted = {'./' + str(PurePosixPath(p).parent) for p in skill_paths if p.split('/')[1] in ['engineering','productivity']}
    registered = json.loads(targets['.claude-plugin/plugin.json'])['skills']
    check(len(registered) == snapshot_counts['promoted'] and set(registered) == promoted, '插件正式技能集合不一致')
    readme_links = links(targets['README.md'])
    indexed = {link.removeprefix('./').removesuffix('/SKILL.md') for link in readme_links if link.endswith('/SKILL.md')}
    check(indexed == {p.removeprefix('./') for p in promoted}, '根 README 技能索引与正式集合不一致')
    for bucket in snapshot_counts['buckets']:
        category = 'skills/' + bucket + '/README.md'
        category_index = {link.removeprefix('./').removesuffix('/SKILL.md') for link in links(targets[category]) if link.endswith('/SKILL.md')}
        category_skills = {PurePosixPath(p).parent.name for p in skill_paths if p.split('/')[1] == bucket}
        check(category_index == category_skills, category + ': 分类索引未完整覆盖技能集合')
    for path in contents:
        if not path.endswith('.md'):
            continue
        if args.partial and path not in REVIEWS:
            continue
        for link in links(contents[path]):
            baseline = local_link_result(path,link,contents)
            translated = local_link_result(path,link,targets)
            if baseline:
                BASELINE_LINKS.append({'path':path,'link':link,'result':baseline})
            elif translated:
                ERRORS.append(path + ': 翻译新增断链 ' + link + ' (' + translated + ')')
    check(git('status','--porcelain=v1').decode() == MANIFEST['source_initial_status'], '源仓库工作区状态改变')
    report = {'mode':'局部' if args.partial else '全量','source_commit':MANIFEST['source_commit'],'paths':len(tree),'skills':len(skill_paths),'reviewed_paths':len(REVIEWS),'reviewed_skills':sum(p.endswith('/SKILL.md') for p in REVIEWS),'preserved_paths':sum(e['method']=='原样保留' for e in entries),'errors':ERRORS,'notes':NOTES,'baseline_links':BASELINE_LINKS,'english_candidates':RESIDUALS,'limitations':['不访问外部 URL；按冻结提交保留上游陈述','自动检查不判断译义；需逐文件全文校对记录','Markdown 采用 CommonMark + table 解析；GitHub 自动锚点算法为本地兼容实现，并补显式锚点','代码模板中的非代码文本改动依靠逐块校对；不会运行示例','HTML 比较标签/属性/嵌套，不运行 CDN 脚本或进行渲染验证','英文逐项保留理由与模板内链接/URL/调用引用由 audit.py 和 english-retained.json 补充验收']}
    (ROOT/'docs/localization/report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['notes','baseline_links','english_candidates']},ensure_ascii=False,indent=2))
    print('上游链接异常/示例候选:',len(BASELINE_LINKS),'英文候选:',len(RESIDUALS))
    return 1 if ERRORS else 0

if __name__ == '__main__':
    sys.exit(main())
