import json
import time
import os

CONFIG_PATH = "/root/Ai-Coder/core/config.json"

class SmartRotator:
    def __init__(self):
        try:
            with open(CONFIG_PATH, "r") as f:
                self.config = json.load(f)
            self.gemini_index = 0
        except Exception as e:
            print(f"❌ Config Error: {e}")

    def get_gemini_key(self):
        return self.config["GEMINI_KEYS"][self.gemini_index]

    def rotate_on_fail(self):
        self.gemini_index = (self.gemini_index + 1) % len(self.config["GEMINI_KEYS"])
        print(f"🔄 Switching to Key #{self.gemini_index}...")
        if self.gemini_index == 0:
            print("⏳ Full cooldown triggered (60s).")
            time.sleep(60)

if __name__ == "__main__":
    rotator = SmartRotator()
    print(f"🚀 Rotator Active. Key: {rotator.get_gemini_key()[:10]}...")
