from crewai.tools import BaseTool
from agents.report_agent import ReportAgent


class ReportTool(BaseTool):
    name: str = "Report Tool"
    description: str = "Generate the final forensic report."

    def _run(self, image_result, ocr_result, ela_result):
        agent = ReportAgent()
        return agent.generate(
            image_result,
            ocr_result,
            ela_result,
        )