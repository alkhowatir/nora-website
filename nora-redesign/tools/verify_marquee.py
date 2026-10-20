import subprocess, json, time, os, urllib.request
from cdp import SimpleWebSocket

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile2')

cmd = [
    chrome_path,
    "--headless=new",
    "--remote-debugging-port=9444",
    f"--user-data-dir={user_data}",
    "--window-size=1440,900",
    f"file:///{os.path.abspath('tools/test_marquee.html').replace(os.sep, '/')}"
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    req = urllib.request.urlopen("http://localhost:9444/json")
    targets = json.loads(req.read().decode())
    page_target = next(t for t in targets if t.get('type') == 'page')
    ws = SimpleWebSocket(page_target['webSocketDebuggerUrl'])

    ws.call("Runtime.enable", {}, 1)

    js_measure = """
    (() => {
        const ltrCard = document.querySelector('.ltr .card');
        const rtlCard = document.querySelector('.rtl .card');
        return {
            ltrLeft: ltrCard.getBoundingClientRect().left,
            rtlLeft: rtlCard.getBoundingClientRect().left
        };
    })()
    """

    raw0 = ws.call("Runtime.evaluate", {"expression": js_measure, "returnByValue": True}, 2)
    print("raw0:", raw0)
    t0 = raw0.get('result', {}).get('value')
    print("t=0s:", t0)
    time.sleep(1)
    raw1 = ws.call("Runtime.evaluate", {"expression": js_measure, "returnByValue": True}, 3)
    t1 = raw1.get('result', {}).get('value')
    print("t=1s:", t1)
    time.sleep(1)
    raw2 = ws.call("Runtime.evaluate", {"expression": js_measure, "returnByValue": True}, 4)
    t2 = raw2.get('result', {}).get('value')
    print("t=2s:", t2)

    ltr_moving_left = t1['ltrLeft'] < t0['ltrLeft']
    rtl_moving_right = t1['rtlLeft'] > t0['rtlLeft']
    print("\nVerification:")
    print("LTR moving right-to-left (decreasing left):", ltr_moving_left, f"({t0['ltrLeft']} -> {t1['ltrLeft']} -> {t2['ltrLeft']})")
    print("RTL moving left-to-right (increasing left):", rtl_moving_right, f"({t0['rtlLeft']} -> {t1['rtlLeft']} -> {t2['rtlLeft']})")

finally:
    proc.terminate()
