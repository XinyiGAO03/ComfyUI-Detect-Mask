import io
import requests
import numpy as np
from PIL import Image
import json 

class YOLOApiNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_url": ("STRING", {"default": "http://localhost:5000/yolo-infer"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("yolo_result",)
    FUNCTION = "call"
    CATEGORY = "YOLO Tools"

    def call(self, image, api_url):
        try:
            i = 255. * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            files = {'image': ('image.png', buffer, 'image/png')}
            res = requests.post(api_url, files=files)

            return (json.dumps(res.json(), indent=2),) if res.ok else (f"Error {res.status_code}: {res.text}",)

        except Exception as e:
            return (f"Exception: {str(e)}",)

NODE_CLASS_MAPPINGS = {
    "YOLOApiNode": YOLOApiNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YOLOApiNode": "YOLO"
}
