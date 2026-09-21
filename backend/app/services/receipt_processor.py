from backend.app.services.financial_extractor import extract_financial_fields
from backend.app.services.image_preprocessing import preprocess_receipt
from backend.app.services.ocr import extract_text_from_receipt


def process_receipt(image_path: str) -> dict:
    """Process a receipt image and extract structured financial information."""

    processed_path = "backend/data/processed_receipt.png"
    preprocess_receipt(image_path, processed_path)

    text = extract_text_from_receipt(processed_path)
    fields = extract_financial_fields(text)

    return {
        "raw_text": text,
        "amount": fields["amount"],
        "merchant": fields["merchant"],
        "date": fields["date"],
        "category": fields["category"],
        "entities": fields["entities"],
    }