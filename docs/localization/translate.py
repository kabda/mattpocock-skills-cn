"""翻译写入与逐批校对登记辅助工具；不执行技能中的指令。"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'docs/localization/manifest.json'

def source(path):
    manifest = json.loads(MANIFEST.read_text())
    entry = next(e for e in manifest['entries'] if e['path'] == path)
    return subprocess.check_output(['git', '-C', manifest['source_path'], 'cat-file', 'blob', entry['source_blob']]).decode()

def fences(text):
    result = []
    lines = text.splitlines(keepends=True)
    start = None
    marker = None
    for i, line in enumerate(lines):
        m = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line)
        if not m:
            continue
        if start is None:
            start, marker = i, m.group(1)
        elif m.group(1)[0] == marker[0] and len(m.group(1)) >= len(marker) and not m.group(2).strip():
            result.append(''.join(lines[start:i+1]).rstrip('\n'))
            start = marker = None
    return result

def write(path, translated):
    original = source(path)
    blocks = fences(original)
    for i, block in enumerate(blocks):
        translated = translated.replace('@@BLOCK' + str(i) + '@@', block)
    if re.search(r'@@BLOCK\d+@@', translated):
        raise ValueError('代码块编号无效: ' + path)
    target = ROOT / path
    target.write_text(translated.strip('\n') + '\n')
    manifest = json.loads(MANIFEST.read_text())
    entry = next(e for e in manifest['entries'] if e['path'] == path)
    entry['status'] = '待校对'
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

def review(paths, note):
    """仅在全文对照完成后调用；校对证据与原译 hash 绑定。"""
    manifest = json.loads(MANIFEST.read_text())
    review_path = ROOT / 'docs/localization/review.json'
    records = json.loads(review_path.read_text())
    for path in paths:
        original = source(path)
        translated = (ROOT / path).read_text()
        records[path] = {
            'source_sha256': hashlib.sha256(original.encode()).hexdigest(),
            'target_sha256': hashlib.sha256(translated.encode()).hexdigest(),
            'review': note,
            'checks': ['全文逐段对照', '前提及规范强度', '术语与触发词', '接口与固定字面量', '链接及代码块用途'],
            'fences': [{'index': i, 'method': '原样代码块' if block in translated else '仅翻译自然语言的代码块，待自动结构检查'} for i, block in enumerate(fences(original))],
        }
        next(e for e in manifest['entries'] if e['path'] == path)['status'] = '已校对待验收'
    review_path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    done = [e for e in manifest['entries'] if e['status'] == '已校对待验收']
    pending = [e['path'] for e in manifest['entries'] if e['status'] in ['尚未处理','待校对']]
    (ROOT / 'docs/localization/progress.md').write_text('# 翻译进度\n\n已全文校对 ' + str(len(done)) + ' 个路径；原样保留项待统一验收。已校对 SKILL.md ' + str(sum(e['path'].endswith('/SKILL.md') for e in done)) + '/38。全部自动验收尚未完成。\n\n最近一批：\n\n' + '\n'.join('- `' + p + '`' for p in paths) + '\n\n待处理路径：\n\n' + '\n'.join('- `' + p + '`' for p in pending) + '\n')

def add_anchors():
    """为已经全文校对的译文补兼容锚点，不改变链接引用目标。"""
    import runpy
    from collections import Counter
    import html
    validation = runpy.run_path(str(ROOT / 'docs/localization/validate.py'))
    parse = validation['tokens']
    slug = validation['slug']
    manifest = json.loads(MANIFEST.read_text())
    records_path = ROOT / 'docs/localization/review.json'
    records = json.loads(records_path.read_text())
    anchor_file = ROOT / 'docs/localization/anchors.json'
    mapping = json.loads(anchor_file.read_text()) if anchor_file.exists() else {}
    pending_writes = []
    for path, record in records.items():
        if not path.endswith('.md'):
            continue
        old = source(path)
        target = ROOT / path
        translated = target.read_text()
        if hashlib.sha256(translated.encode()).hexdigest() != record['target_sha256']:
            raise ValueError('校对后存在未登记修改: ' + path)
        a, b = parse(old), parse(translated)
        ah = [(t,a[i+1]) for i,t in enumerate(a) if t.type == 'heading_open']
        bh = [(t,b[i+1]) for i,t in enumerate(b) if t.type == 'heading_open']
        if [x[0].tag for x in ah] != [x[0].tag for x in bh]:
            raise ValueError('标题层级不能对齐: ' + path)
        offset = len(translated.split('\n---\n',1)[0].splitlines()) + 1 if translated.startswith('---\n') else 0
        lines = translated.splitlines(keepends=True)
        seen = Counter()
        insertions = []
        for (at,ai),(bt,bi) in zip(ah,bh):
            visible = ''.join(c.content for c in ai.children or [] if c.type in ['text','code_inline'])
            key = slug(visible); count = seen[key]; seen[key] += 1
            fragment = key + ('-' + str(count) if count else '')
            if ai.content == bi.content or 'id="' + fragment + '"' in translated:
                continue
            insertions.append((bt.map[0] + offset, '<a id="' + html.escape(fragment,quote=True) + '"></a>\n\n'))
            entry = {'source_heading':ai.content,'translated_heading':bi.content,'fragment':fragment,'method':'在中文标题前添加原 fragment 的显式锚点'}
            if entry not in mapping.setdefault(path,[]):
                mapping[path].append(entry)
        if insertions:
            for line,content in reversed(insertions):
                lines.insert(line,content)
            updated = ''.join(lines)
            pending_writes.append((target, updated))
            record['target_sha256'] = hashlib.sha256(updated.encode()).hexdigest()
            record.setdefault('post_review_changes',[]).append('仅添加 ' + str(len(insertions)) + ' 个源标题兼容锚点；正文未变，映射见 anchors.json')
    if 'docs/localization/anchors.json' not in manifest['additional_path_allowlist']:
        manifest['additional_path_allowlist'].append('docs/localization/anchors.json')
    for target, updated in pending_writes:
        target.write_text(updated)
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    records_path.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    anchor_file.write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n')
    print('已登记兼容锚点:',sum(map(len,mapping.values())))
