import os, re, sys
from pathlib import Path
import http.server
import socketserver
import threading
import urllib.request

SITE = Path(__file__).resolve().parent.parent / 'site'

html_files = list(SITE.glob('**/*.html'))
print(f'Total HTML files found: {len(html_files)}')

broken = []
checked_links = 0

for hf in html_files:
    content = hf.read_text(encoding='utf-8')
    hrefs = re.findall(r'href=[\'"]([^\'"]+)[\'"]', content)
    for href in hrefs:
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'data:')):
            continue
        checked_links += 1
        clean_href = href.split('#')[0].split('?')[0]
        if not clean_href:
            continue
        if clean_href.startswith('/'):
            target = SITE / clean_href.lstrip('/')
        else:
            target = hf.parent / clean_href
            
        if target.is_dir():
            target_file = target / 'index.html'
        else:
            target_file = target
            
        if not target_file.exists():
            broken.append((str(hf.relative_to(SITE)), href, str(target_file)))

print(f'Checked internal links: {checked_links}')
if broken:
    print('Broken links found:')
    for b in broken[:10]:
        print(b)
    sys.exit(1)
else:
    print('ALL INTERNAL LINKS ARE VALID (100% OK)!')

# Now verify via local HTTP server
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

PORT = 8999
os.chdir(SITE)
httpd = socketserver.TCPServer(("", PORT), QuietHandler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()

services = ['architecture', 'interiors', 'furniture', 'identity', 'landscape', 'supervision']
test_paths = [
    '/', '/ar/',
    '/services/', '/ar/services/',
]
for s in services:
    test_paths.append(f'/services/{s}/')
    test_paths.append(f'/ar/services/{s}/')

all_ok = True
for p in test_paths:
    url = f'http://127.0.0.1:{PORT}{p}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            code = resp.getcode()
            if code == 200:
                print(f'200 OK: {p}')
            else:
                print(f'FAIL {code}: {p}')
                all_ok = False
    except Exception as e:
        print(f'ERROR {p}: {e}')
        all_ok = False

httpd.shutdown()

if not all_ok:
    sys.exit(1)
print('ALL HTTP CHECKS PASSED WITH 200 OK!')
