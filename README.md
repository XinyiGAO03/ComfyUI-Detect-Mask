# ComfyUI-Detect-Mask
ComfyUI-Detect-Mask is a custom node package for ComfyUI. This node package contains a variety of different nodes that can help ComfyUI use the YOLO model to identify masks. Specific functions include: sending images to the YOLO API to obtain recognition results, extracting text from web pages, converting YOLO's json results to text, and obtaining sensitive word lists from web pages for sensitive word filtering.

## Function

- **comfyui-online-sensitive**: Load bad word lists from web pages to remove bad worsd in text.
-**comfyui-yolo-api-node**: Send images to the local YOLO-API to obtain JSON results.
- **comfyui_yolo-result_to_text**: Convert the JSON results obtained from YOLO to usable text prompts.
- **comfyui_knowledge_fetcher**: Crawl the information needed from the web page.

## Installation

1. Clone or download this repository into your ComfyUI `custom_nodes` folder:

```bash
https://github.com/XinyiGAO03/ComfyUI-Detect-Mask.git
```

2. Restart ComfyUI.

3. New nodes will appear in the following locations:

- `YOLO Tools`: `YOLO`, `YOLOResultToText`

- `Knowledge Tools`: `WebKnowledgeFetcher`

- `Text/Moderation`: `OnlineSensitiveFilter`

## Node Description

### OnlineSensitiveFilter

Filter bad words online using a customizable bad word list or URL list.

- **Input**:
- `text` (string)
- `badwords_url` (string, provided by default)
- **Output**:
- censored/filtered text (bad words are replaced with "***")
---

### YOLO

Sends an image to a local YOLO inference server and returns the detection results.

- **Input**:
- `image` (image)
- `api_url` (string)
- **Output**:
- JSON detection results

---

### YOLOResultToText

Convert YOLO's JSON results to a structured text format. The converted text can be used for LLM inference.

- **Input**:
- `yolo_json` (string)
- `image_name` (string)
- **Output**:
- Natural language description and reasoning instructions (e.g., YOLO detection result, there are 1 people in the image.
Among them: 1 person is wearing masks incorrectly.)

---

### WebKnowledgeFetcher

Used to fetch and extract relevant paragraph text from one or more web pages. Can be used to help build a knowledge base

- **Input**:
- `url_text` (multi-line string)
- **Output**:
- Extracted web text containing "mask" related content

---

## Use Cases

- Integrate YOLO detection into LLM workflows
- Extract desired content from real web content
- Filter user text in the review process
