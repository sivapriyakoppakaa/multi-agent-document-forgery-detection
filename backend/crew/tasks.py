from crewai import Task
from crew.agents import (
    image_agent,
    ocr_agent,
    ela_agent,
    report_agent
)


def create_tasks():

    image_task = Task(
        description="""
Analyze the document located at {file_path} using your Image Analysis Tool.
Return the image analysis result.
""",
        expected_output="Image analysis JSON.",
        agent=image_agent,
    )

    ocr_task = Task(
        description="""
Extract text from the document located at {file_path} using your OCR Tool.
Return OCR result.
""",
        expected_output="OCR JSON.",
        agent=ocr_agent,
    )

    ela_task = Task(
        description="""
Perform Error Level Analysis on the document located at {file_path}.
Return ELA analysis.
""",
        expected_output="ELA JSON.",
        agent=ela_agent,
    )

    report_task = Task(
        description="""
Using the outputs from the previous agents, generate the final forensic report.
""",
        expected_output="Final forensic report.",
        agent=report_agent,
    )

    return [
        image_task,
        ocr_task,
        ela_task,
        report_task
    ]