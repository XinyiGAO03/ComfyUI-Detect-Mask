import requests
from typing import List

class OnlineSensitiveFilter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "This is an example text."}),
                "badwords_url": ("STRING", {"default": "https://www.cs.cmu.edu/~biglou/resources/bad-words.txt"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("filtered_text",)
    FUNCTION = "filter_text"
    CATEGORY = "Text/Moderation"

    def fetch_bad_words(self, url: str) -> List[str]:
        try:
            response = requests.get(url.strip(), timeout=5)
            response.raise_for_status()
            words = response.text.strip().splitlines()
            return [w.lower() for w in words if w.strip()]
        except Exception as e:
            return [f"[error loading words: {str(e)}]"]

    def filter_text(self, text: str, badwords_url: str) -> tuple:
        badwords = self.fetch_bad_words(badwords_url)
        if badwords and "[error" in badwords[0]:
            return (badwords[0],)

        words = text.split()
        filtered = [
            "***" if w.lower().strip(".,!?") in badwords else w
            for w in words
        ]
        return (" ".join(filtered),)

# 注册节点
NODE_CLASS_MAPPINGS = {
    "OnlineSensitiveFilter": OnlineSensitiveFilter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OnlineSensitiveFilter": "OnlineSensitiveFilter"
}
