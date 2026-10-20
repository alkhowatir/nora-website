import subprocess, json, time, os, urllib.request

# Start Chrome in headless mode with remote debugging
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile')

cmd = [
    chrome_path,
    "--headless=new",
    "--remote-debugging-port=9333",
    f"--user-data-dir={user_data}",
    "--window-size=1440,900",
    "http://localhost:8000/"
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    # Query targets
    targets_url = "http://localhost:9333/json"
    req = urllib.request.urlopen(targets_url)
    targets = json.loads(req.read().decode())
    print("Targets found:", len(targets))
    page_target = next(t for t in targets if t.get('type') == 'page')
    ws_url = page_target['webSocketDebuggerUrl']
    print("WebSocket URL:", ws_url)
finally:
    proc.terminate()
