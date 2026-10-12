from crewai import Agent
from tools.image_tool import ImageAnalysisTool
from tools.ocr_tool import OCRTool
from tools.ela_tool import ELATool
from tools.report_tool import ReportTool
from config.llm import llm
image_agent = Agent(
    role="Image Analysis Expert",
    goal="Analyze uploaded document images for quality, blur, brightness, contrast, and anomalies.",
    backstory="You are an expert in computer vision and image processing.",
    llm=llm,
    tools=[ImageAnalysisTool()],
    verbose=True,
)

ocr_agent = Agent(
    role="OCR Specialist",
    goal="Extract readable text from uploaded documents and evaluate OCR confidence.",
    backstory="You specialize in Optical Character Recognition and document text extraction.",
    tools=[OCRTool()],
    llm=llm,
    verbose=True,
)

ela_agent = Agent(
    role="Forgery Detection Expert",
    goal="Analyze Error Level Analysis (ELA) results to identify possible image manipulation.",
    backstory="You are a digital forensics expert specializing in detecting image tampering.",
    tools=[ELATool()],
    llm=llm,
    verbose=True,
)

report_agent = Agent(
    role="Forensic Report Writer",
    goal="Combine all analysis results into a professional forensic report.",
    backstory="You create forensic investigation reports using outputs from multiple AI agents.",
    tools=[ReportTool()],
    llm=llm,
    verbose=True,
)