# AI-Powered Personal Finance Assistant

An AI-powered personal finance assistant that analyzes personal transactions, forecasts future spending, detects unusual financial activity, and provides personalized financial insights.

## Project Domain

Computer Science & Engineering (AI/ML)

## Core Technologies

- React Native
- FastAPI
- PostgreSQL
- EasyOCR
- Hugging Face Transformers
- PyTorch LSTM
- Scikit-learn
- LangChain
- LLM

## Core Features

- Automatic transaction extraction
- Receipt OCR
- NLP-based transaction information extraction
- Personal expense forecasting
- Anomaly detection
- AI-powered financial advisory

## Synthetic CSV import

The backend can import only synthetic transaction data for development and ML
experiments. Upload a UTF-8 CSV to `POST /transactions/import/csv` using the
form field `file`. Every row is validated before anything is saved, so an
invalid file never creates a partial import.

The required columns are:

```text
amount,transaction_type,category,description,transaction_date,source
```

A sample file is available at `backend/data/synthetic_transactions.csv`.
