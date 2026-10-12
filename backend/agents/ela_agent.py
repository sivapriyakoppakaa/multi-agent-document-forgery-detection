
from utils.ela import perform_ela


class ELAAgent:

    def process(self, image_path):

        try:
            ela = perform_ela(image_path)

            if not isinstance(ela, dict):
                return {
                    "agent": "ELA Agent",
                    "result": {
                        "status": "Manual Review Required",
                        "error": "ELA returned an invalid result."
                    }
                }

            score = float(ela.get("ela_score", 0))

            # Validate the ELA score
            if score < 0:
                return {
                    "agent": "ELA Agent",
                    "result": {
                        "status": "Manual Review Required",
                        "error": "Invalid ELA score."
                    }
                }

            # ELA alone cannot prove a document is genuine.
            # These are preliminary screening thresholds only.
            if score >= 40:
                status = "Potential Manipulation"
            elif score >= 20:
                status = "Manual Review Required"
            else:
                status = "No Strong ELA Anomaly Detected"

            ela["status"] = status
            ela["method"] = "ELA preliminary screening"
            ela["limitations"] = (
                "ELA alone cannot confirm whether a document is "
                "genuine or forged. Interpret with other evidence."
            )

            return {
                "agent": "ELA Agent",
                "result": ela
            }

        except Exception as error:
            return {
                "agent": "ELA Agent",
                "result": {
                    "status": "Manual Review Required",
                    "error": str(error)
                }
            }
