import time

import pyautogui


print("Move your mouse around.")
print("Position will be printed every 2 seconds.")
print("Press Ctrl + C to stop.\n")

try:
    while True:
        x, y = pyautogui.position()
        print(f"Mouse position: x={x}, y={y}")

        time.sleep(2)

except KeyboardInterrupt:
    print("\nStopped.")