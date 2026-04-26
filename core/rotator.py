import json
import base64
import time
import os

ENC_PATH = "/root/Ai-Coder/core/config.enc"

class SmartRotator:
    def __init__(self):
        try:
            with open(ENC_PATH, "r") as f:
                encoded_data = f.read()
                decoded_data = base64.b64decode(encoded_data).decode('utf-8')
                self.config = json.loads(decoded_data)
            self.gemini_index = 0
        except Exception as e:
            print(f"❌ Decryption Error: {e}")

    def get_gemini_key(self):
        return self.config["GEMINI_KEYS"][self.gemini_index]

    def rotate_on_fail(self):
        self.gemini_index = (self.gemini_index + 1) % len(self.config["GEMINI_KEYS"])
        print(f"🔄 Switching to Key #{self.gemini_index}...")

if __name__ == "__main__":
    rotator = SmartRotator()
    print(f"🚀 Rotator Active (Decryption Mode). Version: {rotator.config['VERSION']}")
