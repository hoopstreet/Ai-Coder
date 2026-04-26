import httpx

class GeminiBrain:
    def __init__(self):
        self.api_key = "AIzaSyD0h-VcLh2jBd90O024CPcJUY5Z5lqEVyo"
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={self.api_key}"

    def generate_code(self, prompt, context=""):
        payload = {
            "contents": [{"parts": [{"text": f"Context: {context}\n\nTask: {prompt}\n\nOutput only raw code, no markdown blocks."}]}]
        }
        try:
            r = httpx.post(self.url, json=payload, timeout=30)
            return r.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"Error: {str(e)}"
