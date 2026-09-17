import time

import pyautogui


print("Open Notepad and click inside the text area.")
print("You have 5 seconds...")

time.sleep(5)

pyautogui.write(
    "Hello from AI Overlay!",
    interval=0.05,
)

print("Typing test completed.")