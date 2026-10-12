import cv2
import numpy as np


def analyze_image(image_path):
    image = cv2.imread(image_path)

    if image is None:
        return {"error": "Image not found"}

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    height, width = image.shape[:2]

    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    brightness = np.mean(gray)

    contrast = np.std(gray)

    return {
        "width": width,
        "height": height,
        "blur_score": round(blur_score, 2),
        "brightness": round(brightness, 2),
        "contrast": round(contrast, 2)
    }