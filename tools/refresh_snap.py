#!/usr/bin/env python3
"""index.html 안 미리 넣어 둔 상품 데이터(#snap)를 최신으로 바꿈. 바뀐 게 없으면 파일을 건드리지 않음."""
import json, re, time, urllib.request, pathlib, sys
API = 'https://script.google.com/macros/s/AKfycbwyEpDKKX4pif4FgYtxrepxrqzmCJDM4NmHcb29SrzkMXCPEHMVAwYxdtpEuCwtFCGxyw/exec?action=bootstrap'
f = pathlib.Path(__file__).resolve().parent.parent / 'index.html'
html = f.read_text(encoding='utf-8')
m = re.search(r'(<script type="application/json" id="snap">)(.*?)(</script><!--/snap-->)', html, re.S)
if not m:
    sys.exit('snap 칸이 없습니다')
j = json.load(urllib.request.urlopen(API, timeout=60))
if not j.get('ok') or not j.get('data', {}).get('products'):
    sys.exit('데이터를 받지 못했습니다: %s' % j.get('error'))
try:
    old = json.loads(m.group(2).replace('<\\/', '</'))
except Exception:
    old = None
if old and old.get('d') == j['data']:
    print('변경 없음'); sys.exit(0)
txt = json.dumps({'t': int(time.time() * 1000), 'd': j['data']}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
f.write_text(html[:m.start(2)] + txt + html[m.end(2):], encoding='utf-8')
print('갱신함')
