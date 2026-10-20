import subprocess, json, time, os, urllib.request
from cdp import SimpleWebSocket

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_diag_profile')

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
    targets_url = "http://localhost:9333/json"
    req = urllib.request.urlopen(targets_url)
    targets = json.loads(req.read().decode())
    page_target = next(t for t in targets if t.get('type') == 'page')
    ws = SimpleWebSocket(page_target['webSocketDebuggerUrl'])

    # Enable Runtime and Page
    ws.call("Runtime.enable", {}, 1)
    ws.call("Page.enable", {}, 2)

    # Let the page run for a second
    time.sleep(1)

    # Evaluate JS to inspect the rail elements
    js_diag = """
    (() => {
        const rail = document.querySelector('.rail');
        const track = document.querySelector('.rail-track');
        const groups = document.querySelectorAll('.rail-group');
        const works = document.querySelectorAll('.work');

        const getBox = (el) => {
            if (!el) return null;
            const r = el.getBoundingClientRect();
            const cs = window.getComputedStyle(el);
            return {
                display: cs.display,
                flexDirection: cs.flexDirection,
                flexWrap: cs.flexWrap,
                width: r.width,
                height: r.height,
                top: r.top,
                left: r.left,
                transform: cs.transform
            };
        };

        const workBoxes = Array.from(works).slice(0, 10).map((w, i) => {
            const r = w.getBoundingClientRect();
            return {
                index: i,
                top: Math.round(r.top),
                left: Math.round(r.left),
                width: Math.round(r.width),
                height: Math.round(r.height)
            };
        });

        return {
            rail: getBox(rail),
            track: getBox(track),
            groupCount: groups.length,
            groups: Array.from(groups).map(getBox),
            workCount: works.length,
            works: workBoxes,
            trackTransform: track ? track.style.transform : 'none'
        };
    })()
    """

    res1 = ws.call("Runtime.evaluate", {"expression": js_diag, "returnByValue": True}, 3)
    val1 = res1.get("result", {}).get("value")
    print("Initial Diagnosis:")
    print(json.dumps(val1, indent=2))

    # Wait 2 seconds and measure transform to see if animation is moving
    time.sleep(2)
    res2 = ws.call("Runtime.evaluate", {"expression": js_diag, "returnByValue": True}, 4)
    val2 = res2.get("result", {}).get("value")
    print("\nAfter 2 seconds:")
    print("Track Transform:", val2.get("trackTransform"))

    # Also capture screenshot of the section
    # First scroll the rail into view
    ws.call("Runtime.evaluate", {"expression": "document.querySelector('.rail-wrap').scrollIntoView()"}, 5)
    time.sleep(0.5)
    ss = ws.call("Page.captureScreenshot", {"format": "png"}, 6)
    if ss and "data" in ss:
        import base64
        with open("tools/rail_screenshot.png", "wb") as f:
            f.write(base64.b64decode(ss["data"]))
        print("Saved tools/rail_screenshot.png")

finally:
    proc.terminate()
