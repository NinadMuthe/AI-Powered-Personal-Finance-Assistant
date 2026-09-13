import easyocr


_reader = easyocr.Reader(["en"], gpu=False)


def extract_text_from_receipt(image_path: str) -> str:
    """Extract text from a receipt image using EasyOCR."""
    results = _reader.readtext(image_path, detail=0)

    return "\n".join(results)