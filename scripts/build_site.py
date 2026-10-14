"""Build a static Pages bundle from the locally maintained questionnaire."""
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / '_site'
source = (ROOT / 'questionnaire-compact.html').read_text(encoding='utf-8')
scenes = json.loads(re.search(r'^const SCENES=(.*);$', source, re.M)[1])
images = sorted({path for scene in scenes.values() for path in re.findall(r'src="(img/[^"<>]+)"', scene['html'])})
for path in images:
    resolved = (ROOT / path).resolve()
    if not resolved.is_relative_to(ROOT / 'img') or not resolved.is_file():
        raise ValueError(f'Missing or invalid image: {path}')
# Reference documents and the previous draft remain local.
source = re.sub(r'<a href="3\. questions-and-questionnaire\.pdf"[^>]*>.*?</a> · <a href="questionnaire-irabu\.html"[^>]*>.*?</a>', '', source)
if OUT.exists():
    shutil.rmtree(OUT)
(OUT / 'img').mkdir(parents=True)
(OUT / 'index.html').write_text(source, encoding='utf-8')
(OUT / 'questionnaire-compact.html').write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=./"><a href="./">調査票を開く</a>', encoding='utf-8')
(OUT / '.nojekyll').touch()
for path in images:
    shutil.copy2(ROOT / path, OUT / path)
print(f'Built _site/index.html with {len(images)} images')
