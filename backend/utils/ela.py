
from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import os
import tempfile


def perform_ela(image_path, output_folder="ela_outputs", quality=90):

    os.makedirs(output_folder, exist_ok=True)

    filename = os.path.basename(image_path)
    ela_file = os.path.join(output_folder, "ela_" + filename)

    try:
        with Image.open(image_path) as image:
            original = image.convert("RGB")

        # Recompress the image using JPEG
        with tempfile.NamedTemporaryFile(
            suffix=".jpg",
            dir=output_folder,
            delete=False
        ) as temp:
            temp_file = temp.name

        try:
            original.save(temp_file, "JPEG", quality=quality)

            with Image.open(temp_file) as compressed_image:
                compressed = compressed_image.convert("RGB")

            # Calculate pixel-level differences
            difference = ImageChops.difference(
                original,
                compressed
            )

            diff_array = np.asarray(difference, dtype=np.uint8)

            # Maximum channel difference for each pixel
            pixel_difference = np.max(diff_array, axis=2)

            max_diff = int(pixel_difference.max())

            if max_diff > 0:
                scale = 255.0 / max_diff
                ela_array = np.clip(
                    pixel_difference.astype(np.float32) * scale,
                    0,
                    255
                ).astype(np.uint8)
            else:
                ela_array = np.zeros(
                    pixel_difference.shape,
                    dtype=np.uint8
                )

            ela_image = Image.fromarray(ela_array, mode="L")
            ela_image.save(ela_file)

            # ELA statistics
            ela_score = float(np.mean(ela_array))

            suspicious_pixels = int(
                np.count_nonzero(ela_array > 220)
            )

            total_pixels = ela_array.size

            suspicious_percentage = (
                suspicious_pixels / total_pixels * 100
                if total_pixels else 0.0
            )

            return {
                "ela_image": ela_file,
                "ela_score": round(ela_score, 2),
                "suspicious_percentage": round(
                    suspicious_percentage, 2
                )
            }

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    except Exception as error:
        raise RuntimeError(
            f"ELA analysis failed: {error}"
        ) from error
