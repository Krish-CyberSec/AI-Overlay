import time

from app.windows.hotkey import GlobalHotkey


def on_hotkey():
    print("GLOBAL HOTKEY PRESSED!")


hotkey = GlobalHotkey(on_hotkey)
hotkey.start()

print("Press Ctrl + Shift + Space")
print("Press Ctrl + C to exit")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    hotkey.stop()
    print("\nStopped.")