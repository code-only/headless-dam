# utils/pdf_transform.py
from pdf2image import convert_from_path


def pdf_to_image(input_path: str, output_path: str, page: int = 1, dpi: int = 200):
    images = convert_from_path(input_path, dpi=dpi, first_page=page, last_page=page)
    if images:
        images[0].save(output_path, "JPEG")

