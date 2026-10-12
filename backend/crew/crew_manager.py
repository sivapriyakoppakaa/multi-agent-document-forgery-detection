
from agents.image_agent import ImageAgent
from agents.ocr_agent import OCRAgent
from agents.ela_agent import ELAAgent
from agents.report_agent import ReportAgent


def run_crew(inputs):

    file_path = inputs.get("file_path")

    if not file_path:
        raise ValueError("Missing document file path.")

    # Run the three analysis components
    image_result = ImageAgent().process(file_path)
    ocr_result = OCRAgent().process(file_path)
    ela_result = ELAAgent().process(file_path)

    # Combine the real analysis outputs
    report = ReportAgent().generate(
        image_result,
        ocr_result,
        ela_result
    )

    return report
