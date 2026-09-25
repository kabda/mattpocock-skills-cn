"""补充验收：英文保留项、围栏内链接、URL 与技能调用引用。

与 validate.py 使用相同的隔离依赖命令运行。本脚本不批准新候选；必须与
人工逐项复核后的 english-retained.json 完全一致，新增候选会导致失败。
不执行技能、安装命令、模板代码或远程请求。
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import runpy

ROOT = Path(__file__).resolve().parents[2]
V = runpy.run_path(str(ROOT / 'docs/localization/validate.py'))
MANIFEST = V['MANIFEST']
MD = V['MD']
ENGLISH = re.compile(r"[A-Za-z][A-Za-z'-]*(?:[ \t]+[A-Za-z][A-Za-z'-]*){2,}")
# URL 周围的 Markdown 标点不属于 URL；解析出的链接另外严格比较。
URL = re.compile(r"(?:https?://|mailto:)[A-Za-z0-9:/?#\[\]@!$&*+,;=._~%{}-]+")
INVOCATION = re.compile(r'(?<![A-Za-z0-9_./:<-])([/$][a-z][a-z0-9]*(?:-[a-z0-9]+)*)(?![A-Za-z0-9_./])')
# 人工核对：这两处斜线连接普通名词，不是命令或技能引用。
PROSE_SLASH = {'/include-list', '/build-tool'}


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def collect():
    """生成待比较的事实快照；分类理由另由人工审阅文件提供。"""
    candidates = {}
    fences = []
    preserved = []
    references = []
    errors = []
    url_count = 0
    changed_fence_count = 0
    current_slugs = {Path(e['path']).parent.name for e in MANIFEST['entries'] if e['path'].endswith('/SKILL.md')}

    def scan(path, part, content):
        for match in ENGLISH.finditer(content):
            item = {'path': path, 'part': part, 'text': match.group(), 'context': content}
            key = digest(json.dumps(item, ensure_ascii=False, sort_keys=True))
            if key in candidates:
                candidates[key]['occurrences'] += 1
            else:
                candidates[key] = {'id': key, **item, 'occurrences': 1}

    for entry in MANIFEST['entries']:
        path = entry['path']
        source_bytes = V['git']('cat-file', 'blob', entry['source_blob'])
        source = source_bytes.decode()
        if entry['method'] == '原样保留':
            preserved.append({'path': path, 'mode': entry['mode'], 'sha256': entry['source_sha256']})
            continue
        target = (ROOT / path).read_text()
        if path.endswith('/agents/openai.yaml'):
            scan(path, 'interface.short_description', V['yaml'].safe_load(target)['interface']['short_description'])
        if path.endswith('.json'):
            values = V['flatten'](json.loads(target))
            for field in MANIFEST['mutable_json_paths'].get(path, []):
                scan(path, field, values[field][1])
        if not path.endswith('.md'):
            continue
        frontmatter, _ = V['split_frontmatter'](target)
        if path.endswith('/SKILL.md'):
            for field in ['description', 'argument-hint']:
                if field in frontmatter:
                    scan(path, 'frontmatter.' + field, frontmatter[field])
        if path == 'README.md':
            target = target.removeprefix(MANIFEST['readme_notice'])
        a, b = V['tokens'](source), V['tokens'](target)
        for token in b:
            if token.type == 'inline':
                for child in token.children or []:
                    if child.type in ['text', 'code_inline']:
                        scan(path, child.type, child.content)
        fa, fb = [x for x in a if x.type == 'fence'], [x for x in b if x.type == 'fence']
        if len(fa) != len(fb):
            errors.append(path + ': 围栏数不同')
        for i, (x, y) in enumerate(zip(fa, fb)):
            if x.content == y.content:
                fences.append({'path': path, 'index': i, 'info': x.info, 'sha256': digest(x.content)})
            else:
                changed_fence_count += 1
                for line in y.content.splitlines():
                    scan(path, 'fence:' + str(i), line)
                if Counter(V['links'](x.content)) != Counter(V['links'](y.content)):
                    errors.append(path + ': 模板内部链接变化 ' + str(i))
        ua = Counter(x.rstrip('.,;:!?*)]}') for x in URL.findall(source))
        ub = Counter(x.rstrip('.,;:!?*)]}') for x in URL.findall(target))
        url_count += sum(ua.values())
        if ua != ub:
            errors.append({'path': path, 'kind': 'URL 字面量变化', 'removed': list((ua - ub).elements()), 'added': list((ub - ua).elements())})
        ra = Counter(x for x in INVOCATION.findall(source) if x not in PROSE_SLASH)
        rb = Counter(x for x in INVOCATION.findall(target) if x not in PROSE_SLASH)
        if ra != rb:
            errors.append({'path': path, 'kind': '调用或命令引用变化', 'removed': list((ra - rb).elements()), 'added': list((rb - ra).elements())})
        named = {name: count for name, count in ra.items() if name[1:] in current_slugs}
        if named:
            references.append({'path': path, 'skill_invocations': dict(sorted(named.items()))})
    promoted = {e['path'].split('/')[-2] for e in MANIFEST['entries'] if e['path'].endswith('/SKILL.md') and e['path'].split('/')[1] in ['engineering', 'productivity']}
    docs = {Path(e['path']).stem for e in MANIFEST['entries'] if e['path'].startswith(('docs/engineering/', 'docs/productivity/')) and e['path'].endswith('.md')}
    if promoted != docs:
        errors.append('25 个正式技能与配套 docs 集合不符')
    return {'source_commit': MANIFEST['source_commit'], 'candidates': sorted(candidates.values(), key=lambda x: x['id']),
            'preserved_fences': fences, 'preserved_paths': preserved, 'skill_references': references,
            'promoted_docs': sorted(docs), 'url_occurrences': url_count, 'translated_fences': changed_fence_count, 'errors': errors}


def main():
    snapshot = collect()
    retained_path = ROOT / 'docs/localization/english-retained.json'
    errors = list(snapshot['errors'])
    if not retained_path.exists():
        errors.append('缺少人工复核的英文保留清单')
    else:
        retained = json.loads(retained_path.read_text())
        if retained['source_commit'] != MANIFEST['source_commit']:
            errors.append('英文保留清单源版本不符')
        for section in ['candidates', 'preserved_fences', 'preserved_paths']:
            approved = retained.get(section, [])
            if any(not row.get('reason') for row in approved):
                errors.append(section + ': 存在无保留理由的记录')
            facts = [{k: v for k, v in row.items() if k != 'reason'} for row in approved]
            if facts != snapshot[section]:
                errors.append(section + ': 当前事实与人工复核记录不符，须重新逐项审查')
    report = {'source_commit': MANIFEST['source_commit'], 'errors': errors,
              'reviewed_english_items': len(snapshot['candidates']),
              'english_occurrences': sum(x['occurrences'] for x in snapshot['candidates']),
              'preserved_fences': len(snapshot['preserved_fences']), 'translated_fences': snapshot['translated_fences'],
              'preserved_paths': len(snapshot['preserved_paths']), 'url_occurrences': snapshot['url_occurrences'],
              'promoted_docs': snapshot['promoted_docs'], 'skill_references': snapshot['skill_references'],
              'limitations': ['英文扫描按连续三个以上英文单词找候选，短词和标识另由逐文件全文校对覆盖；扫描不证明译义',
                              '保留英文项必须与手工分类精确匹配；不会自动批准新增候选',
                              'URL 只检查本地字面量，外部地址可用性和平台运行情况未验证',
                              '调用引用扫描排除 HTML 关闭标签和路径连接；include-list/build-tool 两处普通名词连接经人工复核排除。其余 slash/dollar 候选按源译数量比较，当前技能另按冻结树 slug 分类']}
    (ROOT / 'docs/localization/audit-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ['skill_references', 'promoted_docs', 'limitations']}, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == '__main__':
    main()
