from crewai.tools import BaseTool
from agents.ela_agent import ELAAgent


class ELATool(BaseTool):
    name: str = "ELA Tool"
    description: str = "Perform Error Level Analysis."

    def _run(self, file_path: str):
        agent = ELAAgent()
        return agent.process(file_path)