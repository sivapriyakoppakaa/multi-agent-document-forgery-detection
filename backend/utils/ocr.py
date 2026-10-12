import easyocr

# Create the OCR reader only once
reader = easyocr.Reader(['en'])

def extract_text(image_path):
    """
    Extracts text from an image using EasyOCR.
    Returns:
        {
            "text": "...",
            "confidence": 0.95
        }
    """

    results = reader.readtext(image_path)

    extracted_text = []
    confidences = []

    for result in results:
        extracted_text.append(result[1])
        confidences.append(result[2])

    average_confidence = (
        sum(confidences) / len(confidences)
        if confidences else 0
    )

    return {
        "text": "\n".join(extracted_text),
        "confidence": round(average_confidence * 100, 2)
    }