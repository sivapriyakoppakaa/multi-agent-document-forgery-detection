from utils.image_processing import analyze_image


class ImageAgent:

    def process(self, image_path):
        analysis = analyze_image(image_path)

        return {
            "agent": "Image Analysis Agent",
            "result": analysis
        }