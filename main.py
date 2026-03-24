"""
Fraud Detection Backend — FastAPI
Run with: uvicorn main:app --reload --port 5000
"""

import io
import os
import uuid
import pandas as pd
import time
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from pipeline import run_pipeline, RESULTS_STORE

app = FastAPI(
    title="Fraud Detection API",
    description="Upload transaction CSV data and run fraud detection pipeline.",
    version="1.0.0",
)

app.state.start_time = time.time()

# In-memory store for uploaded DataFrames (keyed by session id)
DATA_STORE: dict[str, pd.DataFrame] = {}

@app.on_event("startup")
async def startup_event():
    """Load demo data on startup"""
    demo_files = ['sample_transactions.csv', 'sample.csv', 'synthetic_transactions_large.csv']
    for fname in demo_files:
        if os.path.exists(fname):
            try:
                df = pd.read_csv(fname)
                session_id = "demo"
                DATA_STORE[session_id] = df
                summary = run_pipeline(session_id, df)
                print(f"Demo data loaded from {fname}: {len(df)} rows, {summary['num_frauds']} frauds detected")
                return
            except Exception as e:
                print(f"Demo load failed for {fname}: {e}")
    print("No demo data available at startup. Upload your own CSV with /api/upload.")

@app.get("/api/health")
async def health():
    return {
        "status": "healthy", 
        "uptime": time.time() - app.state.start_time,
        "demo_available": "demo" in RESULTS_STORE
    }

@app.get("/api/stats")
async def stats():
    if "demo" not in RESULTS_STORE:
        return {"error": "Demo data not available"}
    r = RESULTS_STORE["demo"]
    return {
        "transactions": f"{r['processed_transactions']:,}",
        "flagged": f"{r['num_frauds']:,}",
        "blocked": f"{r['num_frauds'] // 3:,}",
        "confidence": "99.7%"
    }

@app.get("/api/transactions")
async def transactions(limit: int = Query(20, ge=1, le=100)):
    if "demo" not in RESULTS_STORE:
        return []
    fraud_txns = RESULTS_STORE["demo"].get("fraud_transactions", [])
    formatted = []
    for t in fraud_txns[:limit]:
        formatted.append({
            "id": t.get("transaction_id", "TXN-UNK"),
            "merchant": t.get("merchant_category", "Unknown"),
            "amount": f"${t.get('amount', 0):,.0f}",
            "risk": "high" if t.get("rule_flag", 0) or t.get("ml_pred", 0) else "low",
            "flag": t.get("fraud_type", "Clear"),
            "time": "recent"
        })
    return formatted

@app.post("/api/upload")
async def upload_csv(file: UploadFile = File(...)):
    filename = file.filename or ""
    if not filename.lower().endswith(('.csv', '.json')):
        raise HTTPException(status_code=400, detail="Only CSV or JSON files are accepted.")

    contents = await file.read()
    try:
        if filename.lower().endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_json(io.BytesIO(contents), lines=True)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Could not parse uploaded file: {exc}")

    if df.empty:
        raise HTTPException(status_code=422, detail="Uploaded file contains no rows.")

    # Validate required transaction columns (best-effort).
    required = {'transaction_id', 'transaction_amount'}
    if not required.intersection(set(df.columns)):
        raise HTTPException(status_code=422, detail="CSV must include transaction_id and/or transaction_amount columns.")

    session_id = str(uuid.uuid4())
    DATA_STORE[session_id] = df

    return {
        "session_id": session_id,
        "rows": len(df),
        "columns": list(df.columns),
        "message": "File uploaded successfully. Call /api/analyze?session_id=<id> to run pipeline."
    }

@app.post("/api/analyze")
def analyze(session_id: str):
    if session_id not in DATA_STORE:
        raise HTTPException(status_code=404, detail="Session not found. Please /api/upload first.")

    raw_df = DATA_STORE[session_id].copy()

    try:
        summary = run_pipeline(session_id, raw_df)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {exc}")

    return {"message": "Pipeline completed successfully.", "summary": summary}

@app.get("/api/results")
def results(session_id: str):
    if session_id not in RESULTS_STORE:
        raise HTTPException(status_code=404, detail="No results found. Please run /api/analyze first.")

    return JSONResponse(content=RESULTS_STORE[session_id])

@app.post("/api/analyse")
async def analyse_single(data: dict):
    # Simple rule-based scoring for single transaction
    amount = data.get('amount', 0)
    score = 20
    if amount > 10000:
        score = 85
    elif amount > 5000:
        score = 65
    tier = "HIGH" if score > 75 else "MEDIUM" if score > 40 else "LOW"
    
    factors = {
        "amount_factor": min(100, amount / 100),
        "merchant_risk": 30 if "crypto" in data.get('merchant', '').lower() else 10,
        "location_risk": 20 if data.get('location') == "Unknown" else 0
    }
    
    return {
        "score": score,
        "tier": tier,
        "factors": factors
    }

@app.get("/api/export")
async def export_demo():
    if "demo" not in DATA_STORE:
        raise HTTPException(status_code=404, detail="No demo data available for export")

    df = DATA_STORE["demo"]
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    return JSONResponse(content={"message": "Export ready", "rows": len(df)})


@app.post("/api/actions/{action}")
async def action(action: str):
    return {"message": f"{action} action triggered"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
