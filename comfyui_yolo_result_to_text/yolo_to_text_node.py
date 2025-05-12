import json

class YOLOResultToText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "yolo_json": ("STRING",),
                "image_name": ("STRING",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("description",)
    FUNCTION = "convert"
    CATEGORY = "YOLO Tools"

    def convert(self, yolo_json, image_name):
        try:
            image_name = image_name or ""
            
            data = json.loads(yolo_json)

            total = data.get("total", 0)
            with_mask = data.get("with_mask", 0)
            without_mask = data.get("without_mask", 0)
            incorrect_mask = data.get("incorrect_mask", 0)

            if total == 0:
                if "replace" in image_name.lower():
                    return (
                        "Input image is a placeholder due to sensitivity concerns.\n"
                        "It is flagged as Not Safe For Work (NSFW).\n"
                        "Please upload a valid image with people wearing masks.",
                    )
                else:
                    return (
                        "No recognizable objects (e.g., people wearing masks) were detected in the image.\n"
                        "Please upload a different image that includes visible individuals.",
                    )

            parts = []
            parts.append(f"YOLO detection result, there are {total} people in the image.")
            parts.append(f"\n Among them:")
            if with_mask > 0:
                parts.append(f"{with_mask} {'person is' if with_mask == 1 else 'people are'} wearing masks correctly.")
            if incorrect_mask > 0:
                parts.append(
                    f"{incorrect_mask} {'person is' if incorrect_mask == 1 else 'people are'} wearing masks incorrectly.")
            if without_mask > 0:
                parts.append(f"{without_mask} {'person is' if without_mask == 1 else 'people are'} not wearing a mask.")

            # 添加推理任务指令
            parts.append("\nBased on the YOLO detection and image itself, answer the following:")
            parts.append(
                "1. The mask-wearing status detected by YOLO must be strictly followed. Do NOT contradict it.")
            parts.append("2. What is the mask’s type?")

            return (" ".join(parts),)

        except Exception as e:
            return (f"Failed to parse YOLO output: {str(e)}",)


NODE_CLASS_MAPPINGS = {
    "YOLOResultToText": YOLOResultToText
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YOLOResultToText": "YOLOResultToText"
}
