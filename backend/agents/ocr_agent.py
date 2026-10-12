from utils.ocr import extract_text


class OCRAgent:

    def process(self, image_path):
        ocr = extract_text(image_path)

        return {
            "agent": "OCR Agent",
            "result": ocr
        }