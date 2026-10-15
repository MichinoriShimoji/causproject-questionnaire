"""Promote only questionnaire definitions from a browser backup into HTML.
Usage: python3 scripts/sync_questionnaire.py /path/to/backup.json
Responses, notes, identities, dates and progress are never copied.
"""
import json
from pathlib import Path
import re
import sys
from collections import Counter
ROOT = Path(__file__).resolve().parent.parent
path = ROOT / 'questionnaire-compact.html'
source = path.read_text(encoding='utf-8')
backup = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
data = json.loads(re.search(r'^const DATA=(.*);$', source, re.M)[1])
scenes = json.loads(re.search(r'^const SCENES=(.*);$', source, re.M)[1])
scene_map = json.loads(re.search(r'^const SCENE_MAP=(.*);$', source, re.M)[1])
if backup.get('custom'):
    raise ValueError('Custom cards require explicit mapping before publication.')
allowed = {'stimulus', 'translation', 'priority'}
for q in data:
    a = backup.get('answers', {}).get(str(q['n']), {})
    for field in allowed:
        if field in a:
            if not isinstance(a[field], str):
                raise ValueError(f'Invalid {field}')
            if field == 'priority' and a[field] not in ('A', 'B', 'C'):
                raise ValueError('Invalid priority')
            q[field] = a[field]
    q.setdefault('priority', 'B')
    if 'scene' in a:
        if a['scene'] and a['scene'] not in scenes:
            raise ValueError('Unknown scene')
        scene_map[str(q['n'])] = [a['scene']] if a['scene'] else []
source = re.sub(r'^const DATA=.*;$', lambda _: 'const DATA='+json.dumps(data, ensure_ascii=False)+';', source, flags=re.M)
source = re.sub(r'^const SCENE_MAP=.*;$', lambda _: 'const SCENE_MAP='+json.dumps(scene_map, ensure_ascii=False)+';', source, flags=re.M)
source = source.replace("function priority(q){return state.answers[q.n]?.priority||'B';}", "function priority(q){return state.answers[q.n]?.priority||q.priority||'B';}")
source = source.replace('未指定の優先度はB。', '優先度は配布版の設定が初期値です。')
# Keep the existing local authoring inputs consistent with the published source.
work = ROOT / '.work'
if work.exists():
    (work / 'data.json').write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    template = re.sub(r'^const DATA=.*;$', lambda _: 'const DATA=__DATA__;', source, flags=re.M)
    (work / 'app.html').write_text(template, encoding='utf-8')
path.write_text(source, encoding='utf-8')
removed = {8, 9, 22, 23, '23-2', '23-6', '23-7', '23-8'}
counts = Counter(q['priority'] for q in data if q['n'] not in removed)
print('Published default priorities:', dict(sorted(counts.items())))
print('Copied only stimulus, translation, priority, scene. No responses or identity data.')
