from PIL import Image, ImageEnhance, ImageFilter


def preprocess_receipt(image_path: str, output_path: str) -> str:
    """Preprocess a receipt image to improve OCR quality."""

    image = Image.open(image_path).convert("L")

    # Increase contrast
    image = ImageEnhance.Contrast(image).enhance(2.0)

    # Sharpen text
    image = image.filter(ImageFilter.SHARPEN)

    image.save(output_path)

    return output_path