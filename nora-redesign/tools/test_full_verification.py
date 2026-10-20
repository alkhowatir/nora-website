import subprocess, json, time, os, urllib.request
from cdp import SimpleWebSocket

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_full')

def run_tests():
    cmd = [
        chrome_path,
        "--headless=new",
        "--remote-debugging-port=9445",
        f"--user-data-dir={user_data}",
        "--window-size=1440,900"
    ]
    proc = subprocess.Popen(cmd)
    time.sleep(2)

    try:
        req = urllib.request.urlopen("http://localhost:9445/json")
        targets = json.loads(req.read().decode())
        page_target = next(t for t in targets if t.get('type') == 'page')
        ws = SimpleWebSocket(page_target['webSocketDebuggerUrl'])

        msg_id = 1
        def call(method, params=None):
            nonlocal msg_id
            msg_id += 1
            return ws.call(method, params or {}, msg_id)

        call("Runtime.enable")
        call("Page.enable")

        results = {}

        # Test cases: (name, url, width, height, expected_dir)
        # expected_dir: 'ltr_motion' means left decreases (right to left)
        #               'rtl_motion' means left increases (left to right)
        test_cases = [
            ("Desktop AR (1440x900)", "http://localhost:8000/", 1440, 900, "rtl_motion"),
            ("Desktop EN (1440x900)", "http://localhost:8000/en/", 1440, 900, "ltr_motion"),
            ("Mobile AR (390x844)", "http://localhost:8000/", 390, 844, "rtl_motion"),
            ("Mobile EN (390x844)", "http://localhost:8000/en/", 390, 844, "ltr_motion")
        ]

        for name, url, w, h, exp_motion in test_cases:
            print(f"\n================ Running test: {name} ================")
            call("Emulation.setDeviceMetricsOverride", {
                "width": w,
                "height": h,
                "deviceScaleFactor": 1,
                "mobile": (w < 600)
            })

            call("Page.navigate", {"url": url})
            time.sleep(2)

            # 1. Check console errors
            # 2. Check layout (horizontal single row)
            # 3. Check movement over 2 seconds
            check_js = """
            (() => {
                const rail = document.querySelector('.rail');
                const groups = document.querySelectorAll('.rail-group');
                const firstGroupCards = groups[0] ? Array.from(groups[0].querySelectorAll('.work')) : [];
                
                const cardTops = firstGroupCards.map(c => Math.round(c.getBoundingClientRect().top));
                const allSameTop = cardTops.length > 0 && cardTops.every(t => Math.abs(t - cardTops[0]) < 2);

                const cardWidths = firstGroupCards.map(c => Math.round(c.getBoundingClientRect().width));
                
                return {
                    groupsCount: groups.length,
                    cardsCount: firstGroupCards.length,
                    allSameTop: allSameTop,
                    cardTopsSample: cardTops.slice(0, 4),
                    cardWidthSample: cardWidths[0],
                    firstCardLeft: firstGroupCards[0] ? firstGroupCards[0].getBoundingClientRect().left : null,
                    secondCardLeft: firstGroupCards[1] ? firstGroupCards[1].getBoundingClientRect().left : null,
                    group0Left: groups[0] ? groups[0].getBoundingClientRect().left : null,
                    group1Left: groups[1] ? groups[1].getBoundingClientRect().left : null
                };
            })()
            """
            d0 = call("Runtime.evaluate", {"expression": check_js, "returnByValue": True})['result']['value']
            time.sleep(1.5)
            d1 = call("Runtime.evaluate", {"expression": check_js, "returnByValue": True})['result']['value']

            pos0 = d0['group0Left']
            pos1 = d1['group0Left']
            delta = pos1 - pos0

            is_horizontal = d0['allSameTop']
            if exp_motion == 'rtl_motion':
                # Arabic: left-to-right means pos1 > pos0 (delta > 0)
                is_moving_correctly = delta > 0
                direction_str = "left-to-right (increasing X)"
            else:
                # English: right-to-left means pos1 < pos0 (delta < 0)
                is_moving_correctly = delta < 0
                direction_str = "right-to-left (decreasing X)"

            print(f"Cards in single row (all same top): {is_horizontal} (tops: {d0['cardTopsSample']})")
            print(f"Card width: {d0['cardWidthSample']}px")
            print(f"Movement delta over 1.5s: {delta:.2f}px")
            print(f"Expected motion: {direction_str} -> Passed: {is_moving_correctly}")

            # Capture screenshot
            img_res = call("Page.captureScreenshot", {"format": "png"})
            import base64
            safe_name = name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("x", "_")
            out_img = f"tools/{safe_name}.png"
            with open(out_img, "wb") as f:
                f.write(base64.b64decode(img_res['result']['data']))
            print(f"Saved screenshot: {out_img}")

            results[name] = {
                "horizontal_single_row": is_horizontal,
                "moving_correctly": is_moving_correctly,
                "delta": delta,
                "card_width": d0['cardWidthSample']
            }

        # Test hover pause on Desktop AR
        print("\n================ Testing Hover Pause on Desktop AR ================")
        call("Emulation.setDeviceMetricsOverride", {
            "width": 1440,
            "height": 900,
            "deviceScaleFactor": 1,
            "mobile": False
        })
        call("Page.navigate", {"url": "http://localhost:8000/"})
        time.sleep(1.5)

        # Scroll to rail and hover
        hover_js = """
        (() => {
            const rail = document.querySelector('.rail');
            rail.scrollIntoView({ block: 'center' });
            return rail.getBoundingClientRect();
        })()
        """
        rail_rect = call("Runtime.evaluate", {"expression": hover_js, "returnByValue": True})['result']['value']
        
        # Dispatch mouse move over rail
        call("Input.dispatchMouseEvent", {
            "type": "mouseMoved",
            "x": rail_rect['left'] + 100,
            "y": rail_rect['top'] + 100
        })
        time.sleep(0.5)

        # Check position over 1 second while hovered
        p_h0 = call("Runtime.evaluate", {"expression": "document.querySelector('.rail-group').getBoundingClientRect().left", "returnByValue": True})['result']['value']
        time.sleep(1.0)
        p_h1 = call("Runtime.evaluate", {"expression": "document.querySelector('.rail-group').getBoundingClientRect().left", "returnByValue": True})['result']['value']
        hover_paused = abs(p_h1 - p_h0) < 0.5
        print(f"Hover pause check: p0={p_h0:.2f}, p1={p_h1:.2f}, delta={abs(p_h1 - p_h0):.2f}px -> Paused: {hover_paused}")

        results["Hover Pause (Desktop AR)"] = hover_paused

        # Test Prefers-reduced-motion
        print("\n================ Testing prefers-reduced-motion ================")
        call("Emulation.setEmulatedMedia", {"media": "", "features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
        time.sleep(0.5)
        p_rm0 = call("Runtime.evaluate", {"expression": "document.querySelector('.rail-group').getBoundingClientRect().left", "returnByValue": True})['result']['value']
        time.sleep(1.0)
        p_rm1 = call("Runtime.evaluate", {"expression": "document.querySelector('.rail-group').getBoundingClientRect().left", "returnByValue": True})['result']['value']
        reduced_motion_paused = abs(p_rm1 - p_rm0) < 0.5
        print(f"Reduced motion check: p0={p_rm0:.2f}, p1={p_rm1:.2f}, delta={abs(p_rm1 - p_rm0):.2f}px -> Paused: {reduced_motion_paused}")

        results["prefers-reduced-motion"] = reduced_motion_paused

        print("\n================ SUMMARY RESULTS ================")
        print(json.dumps(results, indent=2))

    finally:
        proc.terminate()

if __name__ == '__main__':
    run_tests()
