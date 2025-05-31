# utils/image_transform.py
from PIL import Image
import io


def transform_image(
    input_path: str,
    output_path: str,
    width: int = None,
    height: int = None,
    crop: bool = False,
    format: str = None,
    quality: int = 80,
):
    """
    Transform an image by resizing, cropping, and changing format.
    :param input_path: Path to the input image file.
    :param output_path: Path to save the transformed image.
    :param width: Desired width of the output image (None for no resize).
    :param height: Desired height of the output image (None for no resize).
    :param crop: If True, crop the image to the specified width and height.
    :param format: Desired output format (e.g., 'JPEG', 'PNG'). If None, keeps original format.
    :param quality: Quality of the output image (1-100, default is 80).
    """
    with Image.open(input_path) as img:
        orig_format = img.format
        if width and height:
            if crop:
                img = img.crop((0, 0, width, height))
            else:
                img = img.resize((width, height))
        elif width or height:
            img.thumbnail((width or img.width, height or img.height))
        img.save(output_path, format=format or orig_format, quality=quality)

