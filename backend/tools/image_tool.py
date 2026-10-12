from crewai.tools import BaseTool
from agents.image_agent import ImageAgent


class ImageAnalysisTool(BaseTool):
    name: str = "Image Analysis Tool"
    description: str = "Analyzes uploaded document images using OpenCV."

    def _run(self, file_path: str):
        agent = ImageAgent()
        return agent.process(file_path)