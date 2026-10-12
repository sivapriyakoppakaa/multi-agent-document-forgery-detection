import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_ai_report(image_result, ocr_result, ela_result):

    # Keep OCR text short to avoid huge prompts
    ocr_text = ocr_result["result"]["text"][:300]

    prompt = f"""
You are an expert AI document forensic analyst.

Analyze the following document analysis results.

Image Analysis:
- Blur Score: {image_result["result"]["blur_score"]}
- Brightness: {image_result["result"]["brightness"]}
- Contrast: {image_result["result"]["contrast"]}

OCR Analysis:
- Confidence: {ocr_result["result"]["confidence"]}%
- Extracted Text (Preview):
{ocr_text}

ELA Analysis:
- Score: {ela_result["result"]["ela_score"]}
- Suspicious Pixels: {ela_result["result"]["suspicious_percentage"]}%
- Status: {ela_result["result"]["status"]}

Generate a clear and concise forensic report.

Use exactly this structure:

FINAL VERDICT: Likely Genuine / Low Suspicion

IMAGE QUALITY:
Good image quality. Blur Score: 1354.49, Brightness: 166.82,
Contrast: 54.52.

OCR FINDINGS:
OCR confidence is 12.03%, which is low. Text extraction is unreliable.

ELA FINDINGS:
ELA Score: 9.88
Suspicious Regions: 0.0%
Status: Low Suspicion

OVERALL ASSESSMENT:
No clear evidence of digital manipulation was detected.
However, the low OCR confidence means manual verification is recommended.

RECOMMENDATION:
Compare the document with an original or official record.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"AI report could not be generated.\nError: {str(e)}"