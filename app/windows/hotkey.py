from pynput import keyboard


class GlobalHotkey:
    def __init__(self, callback):
        self.callback = callback
        self.listener = keyboard.GlobalHotKeys({
            "<ctrl>+<shift>+<space>": self.callback
        })

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()