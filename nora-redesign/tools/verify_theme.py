import subprocess, json, time, os, urllib.request
from cdp import SimpleWebSocket

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_theme')

def test_theme():
    cmd = [
        chrome_path,
        "--headless=new",
        "--remote-debugging-port=9446",
        f"--user-data-dir={user_data}",
        "--window-size=1440,900"
    ]
    proc = subprocess.Popen(cmd)
    time.sleep(2)

    try:
        req = urllib.request.urlopen("http://localhost:9446/json")
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

        # Emulate OS system preference = DARK
        call("Emulation.setEmulatedMedia", {
            "media": "",
            "features": [{"name": "prefers-color-scheme", "value": "dark"}]
        })

        urls = ["http://localhost:8000/", "http://localhost:8000/en/"]

        for u in urls:
            print(f"\nTesting URL with OS dark-mode enabled: {u}")
            call("Page.navigate", {"url": u})
            time.sleep(1.5)

            # Clear any previously saved localStorage key to test brand-new visitor
            clear_script = "localStorage.removeItem('nora-theme');"
            call("Runtime.evaluate", {"expression": clear_script})
            # Reload page to test first visit with OS dark mode
            call("Page.navigate", {"url": u})
            time.sleep(1.5)

            check_script = """
            (() => {
                return {
                    osPrefersDark: window.matchMedia('(prefers-color-scheme: dark)').matches,
                    themeAttr: document.documentElement.dataset.theme,
                    metaTheme: document.querySelector('meta[name="theme-color"]').getAttribute('content'),
                    savedTheme: localStorage.getItem('nora-theme'),
                    toggleExists: !!document.querySelector('.theme-toggle')
                };
            })()
            """
            res = call("Runtime.evaluate", {"expression": check_script, "returnByValue": True})['result']['value']
            print("Initial state for new visitor:", res)
            assert res['themeAttr'] == 'light', f"Expected light theme, got {res['themeAttr']}"
            assert res['metaTheme'] == '#e9e5dc', f"Expected light meta theme, got {res['metaTheme']}"
            print("=> Verified: Default theme is light mode despite OS prefers-color-scheme: dark!")

            # Now test manual toggle to dark mode
            toggle_script = """
            (() => {
                const btn = document.querySelector('.theme-toggle');
                btn.click();
                return {
                    themeAttr: document.documentElement.dataset.theme,
                    metaTheme: document.querySelector('meta[name="theme-color"]').getAttribute('content'),
                    savedTheme: localStorage.getItem('nora-theme'),
                    ariaChecked: btn.getAttribute('aria-checked')
                };
            })()
            """
            res2 = call("Runtime.evaluate", {"expression": toggle_script, "returnByValue": True})['result']['value']
            print("After clicking theme toggle once:", res2)
            assert res2['themeAttr'] == 'dark', f"Expected dark theme after toggle, got {res2['themeAttr']}"
            assert res2['savedTheme'] == 'dark', f"Expected localStorage dark, got {res2['savedTheme']}"
            assert res2['metaTheme'] == '#0a0c0e', f"Expected dark meta theme, got {res2['metaTheme']}"
            assert res2['ariaChecked'] == 'true', f"Expected aria-checked true, got {res2['ariaChecked']}"
            print("=> Verified: Manual switch to dark mode works!")

            # Toggle back to light mode
            res3 = call("Runtime.evaluate", {"expression": toggle_script, "returnByValue": True})['result']['value']
            print("After clicking theme toggle twice (back to light):", res3)
            assert res3['themeAttr'] == 'light', f"Expected light theme after toggle, got {res3['themeAttr']}"
            assert res3['savedTheme'] == 'light', f"Expected localStorage light, got {res3['savedTheme']}"
            assert res3['metaTheme'] == '#e9e5dc', f"Expected light meta theme, got {res3['metaTheme']}"
            assert res3['ariaChecked'] == 'false', f"Expected aria-checked false, got {res3['ariaChecked']}"
            print("=> Verified: Manual switch back to light mode works!")

        print("\nAll theme tests passed successfully!")

    finally:
        proc.terminate()

if __name__ == '__main__':
    test_theme()
