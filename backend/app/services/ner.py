from transformers import pipeline


_ner_pipeline = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple",
)


def extract_entities(text: str) -> list[dict]:
    """Extract named entities from OCR text."""
    if not text.strip():
        return []

    results = _ner_pipeline(text)

    return [
        {
            "entity": result["entity_group"],
            "text": result["word"],
            "score": round(float(result["score"]), 4),
        }
        for result in results
    ]