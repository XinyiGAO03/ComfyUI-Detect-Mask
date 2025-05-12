import requests
from bs4 import BeautifulSoup
from typing import List

class WebKnowledgeFetcherNode:
    INPUT_TYPES = lambda: {
        "required": {
            "url_text": ("STRING", {"multiline": True, "default": "https://en.wikipedia.org/wiki/Surgical_mask"})
        }
    }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("knowledge_text",)
    FUNCTION = "run"
    CATEGORY = "Knowledge Tools"

    def __init__(self):
        self.max_chars = 100000  # 可调节网页内容提取上限

    def fetch_and_clean(self, url: str) -> str:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = requests.get(url.strip(), headers=headers, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")

            # 只保留包含“mask”的段落（忽略大小写）
            filtered = [
                p.get_text(strip=True) for p in paragraphs
                if "mask" in p.get_text(strip=True).lower()
            ]

            clean_text = "\n".join(filtered)
            return clean_text.strip()

        except Exception as e:
            return f"[Error fetching {url.strip()}]: {str(e)}"

    def fetch_multiple(self, urls: List[str]) -> str:
        contents = []
        for url in urls:
            text = self.fetch_and_clean(url)
            contents.append(f"From {url.strip()}:")
            contents.append(text)
        full_knowledge = "\n\n".join(contents)
        return f"Knowledge Base:\n{full_knowledge[:self.max_chars].strip()}"

    def run(self, url_text: str):
        url_list = [line for line in url_text.strip().splitlines() if line.strip()]
        knowledge = self.fetch_multiple(url_list)
        return (knowledge,)

NODE_CLASS_MAPPINGS = {
    "WebKnowledgeFetcher": WebKnowledgeFetcherNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WebKnowledgeFetcher": "WebKnowledgeFetcher"
}
