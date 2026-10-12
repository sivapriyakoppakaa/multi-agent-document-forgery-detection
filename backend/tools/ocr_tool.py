from crewai.tools import BaseTool
from agents.ocr_agent import OCRAgent


class OCRTool(BaseTool):
    name: str = "OCR Tool"
    description: str = "Extract text from uploaded documents."

    def _run(self, file_path: str):
        agent = OCRAgent()
        return agent.process(file_path)