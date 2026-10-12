
import json
from utils.llm import generate_ai_report


def normalize_result(value):
    if isinstance(value, dict):
        return value

    if isinstance(value, str):
        value = value.strip()

        if value.startswith("```"):
            lines = value.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            value = "\n".join(lines).strip()

        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

    raise ValueError("Agent output is not a valid JSON object.")


class ReportAgent:

    def generate(self, image_result, ocr_result, ela_result):

        try:
            image_result = normalize_result(image_result)
            ocr_result = normalize_result(ocr_result)
            ela_result = normalize_result(ela_result)

            image_data = image_result.get("result", image_result)
            ocr_data = ocr_result.get("result", ocr_result)
            ela_data = ela_result.get("result", ela_result)

            required = (
                "blur_score" in image_data
                and "confidence" in ocr_data
                and "ela_score" in ela_data
            )

            if not required or any(
                "error" in data
                for data in (image_data, ocr_data, ela_data)
            ):
                raise ValueError("One or more agent results are missing.")

            blur = float(image_data["blur_score"])
            confidence = float(ocr_data["confidence"])
            ela_score = float(ela_data["ela_score"])
            suspicious_percentage = float(
                ela_data.get("suspicious_percentage", 0)
            )

            if (
                blur < 0
                or not 0 <= confidence <= 100
                or ela_score < 0
                or not 0 <= suspicious_percentage <= 100
            ):
                raise ValueError("Invalid analysis values.")

            reasons = []

            # Image quality indicates reliability, not authenticity.
            quality_ok = blur >= 100

            if quality_ok:
                reasons.append("Image passed the preliminary sharpness check.")
            else:
                reasons.append(
                    "Image may be too blurry for reliable analysis."
                )

            if confidence < 40:
                reasons.append(
                    "OCR confidence is low; extracted text may be unreliable."
                )
            else:
                reasons.append(
                    f"OCR extraction confidence: {confidence:.1f}%."
                )

            # Preliminary screening thresholds; not validated classifiers.
            ela_flag = (
                ela_score >= 40
                or suspicious_percentage >= 5
            )

            if ela_flag:
                reasons.append(
                    "ELA indicates potential image anomalies requiring review."
                )
            else:
                reasons.append(
                    "ELA did not cross the preliminary anomaly thresholds."
                )

            # Do not confuse this heuristic score with probability of authenticity.
            score = 50

            if quality_ok:
                score += 10
            else:
                score -= 10

            if confidence >= 60:
                score += 5
            elif confidence < 20:
                score -= 5

            if ela_flag:
                score -= 20

            score = max(0, min(100, score))

            if not quality_ok or confidence < 20:
                status = "Manual Review Required"
            elif ela_flag:
                status = "Potential Manipulation"
            else:
                status = "No Strong Signs Detected"

            try:
                ai_summary = generate_ai_report(
                    image_result,
                    ocr_result,
                    ela_result
                )
            except Exception as error:
                print("AI report generation failed:", error)
                ai_summary = (
                    "Automated analysis completed. The AI narrative "
                    "could not be generated; review the findings manually."
                )

            return {
                "status": status,
                "trust_score": score,
                "score_type": "Preliminary heuristic screening score",
                "reasons": reasons,
                "ai_summary": ai_summary,
                "image_analysis": image_data,
                "ocr_analysis": {
                    "confidence": confidence,
                    "text": ocr_data.get("text", "")
                },
                "ela_analysis": ela_data
            }

        except (TypeError, ValueError, KeyError) as error:
            return {
                "status": "Manual Review Required",
                "trust_score": None,
                "score_type": "Not calculated",
                "reasons": [str(error)],
                "ai_summary": (
                    "The analysis results were invalid or incomplete. "
                    "Manual verification is required."
                )
            }
