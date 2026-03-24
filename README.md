# Fraud Detection API

A modular FastAPI backend for detecting financial transaction fraud using rule-based heuristics and a RandomForest machine learning model.

---

## Project Structure

```
fraud_detection/
├── main.py                  # FastAPI app — defines /upload, /analyze, /results
├── pipeline.py              # All processing stages (cleaning → ML → classification)
├── generate_sample_data.py  # Creates sample_transactions.csv for testing
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) Generate sample data
```bash
python generate_sample_data.py
# → sample_transactions.csv  (~1410 rows × 16 columns)
```

### 3. Start the server
```bash
uvicorn main:app --reload
```

Server runs at **http://127.0.0.1:8000**  
Interactive docs at **http://127.0.0.1:8000/docs**

---

## API Reference

### `POST /upload`
Upload a CSV file of transactions.

```bash
curl -X POST "http://127.0.0.1:8000/upload" \
  -F "file=@sample_transactions.csv"
```

**Response**
```json
{
  "session_id": "f3a1...",
  "rows": 1410,
  "columns": ["transaction_id", "user_id", ...],
  "message": "File uploaded successfully. Call /analyze?session_id=<id> to run the pipeline."
}
```

---

### `POST /analyze?session_id=<id>`
Run the full fraud-detection pipeline.

```bash
curl -X POST "http://127.0.0.1:8000/analyze?session_id=f3a1..."
```

**Response**
```json
{
  "message": "Pipeline completed successfully.",
  "summary": {
    "total_transactions": 1400,
    "num_frauds": 98,
    "fraud_percentage": 7.0,
    "precision": 0.8421,
    "recall": 0.7647,
    "f1_score": 0.8015
  }
}
```

---

### `GET /results?session_id=<id>`
Retrieve the full fraud report including individual fraud transactions.

```bash
curl "http://127.0.0.1:8000/results?session_id=f3a1..."
```

**Response**
```json
{
  "total_transactions": 1400,
  "num_frauds": 98,
  "fraud_percentage": 7.0,
  "precision": 0.8421,
  "recall": 0.7647,
  "f1_score": 0.8015,
  "fraud_transactions": [
    {
      "transaction_id": "TXN000042",
      "user_id": "U0017",
      "amount": 12540.5,
      "rule_flag": 1,
      "ml_pred": 1,
      "fraud_type": "High Amount Fraud",
      ...
    }
  ]
}
```

---

## Pipeline Stages

| Stage | Module function | Description |
|---|---|---|
| 1 | `clean_data` | Dedup, parse datetimes, impute NaN, label-encode |
| 2 | `engineer_features` | Frequency, avg amount, time-diff, device count, high-value flag |
| 3 | `rule_based_detection` | High amount / velocity / behavioural-anomaly rules → `rule_flag` |
| 4 | `train_and_predict` | RandomForest (80/20 split, balanced classes) → `ml_pred` |
| 5 | `add_fraud_type` | Maps each flagged row to a fraud category → `fraud_type` |

## Fraud Type Categories

| Type | Trigger |
|---|---|
| **High Amount Fraud** | `is_high_value == 1` and flagged |
| **Velocity Fraud** | Frequency > 10 AND time between txns < 60 s |
| **Behavioral Anomaly** | Flagged but not high-amount or velocity |
| **Normal** | Not flagged by either rule or ML |

---

## CSV Column Requirements

The pipeline auto-detects columns by name. At minimum the CSV should contain:
- A **user/account identifier** column (e.g. `user_id`, `customer_id`)
- A **transaction amount** column (e.g. `amount`, `transaction_amount`)
- A **timestamp** column in any standard datetime format

Optional columns that improve detection:
- `device_id` — enables device-count feature
- `fraud` — use real labels; otherwise synthesised from rule_flag
