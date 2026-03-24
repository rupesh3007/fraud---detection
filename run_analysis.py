import requests
import sys
import json
import pandas as pd
from io import BytesIO

def analyze_csv(csv_path, api_url='http://localhost:5000'):
    # Read CSV
    df = pd.read_csv(csv_path)
    print(f"📊 Loaded {len(df)} transactions")
    
    # Step 1: Upload
    try:
        with open(csv_path, 'rb') as f:
            files = {'file': (csv_path, f, 'text/csv')}
            response = requests.post(f'{api_url}/api/upload', files=files, timeout=20)
    except requests.exceptions.RequestException as exc:
        print(f"❌ Upload failed (connection issue): {exc}")
        return
    except FileNotFoundError:
        print(f"❌ Upload failed: file not found: {csv_path}")
        return

    if response.status_code != 200:
        print(f"❌ Upload failed: {response.text}")
        return
    
    data = response.json()
    session_id = data['session_id']
    print(f"✅ Uploaded! Session ID: {session_id}")
    
    # Step 2: Analyze
    response = requests.post(f'http://localhost:5000/api/analyze?session_id={session_id}')
    if response.status_code != 200:
        print(f"❌ Analyze failed: {response.text}")
        return
    
    print("🔍 Analysis complete!")
    
    # Step 3: Get results
    response = requests.get(f'http://localhost:5000/api/results?session_id={session_id}')
    results = response.json()
    
    # Print formatted JSON
    print("\n📈 FRAUD ANALYSIS RESULTS:")
    print(json.dumps(results, indent=2))
    
    # Summary table
    print("\n📊 SUMMARY TABLE:")
    print(f"{'='*50}")
    print(f"Total Transactions: {results['processed_transactions']:,}")
    print(f"Fraud Count: {results['num_frauds']:,}")
    print(f"Fraud Rate: {results['fraud_percentage']:.2f}%")
    print(f"Model F1 Score: {results['f1_score']:.4f}")
    print(f"Precision: {results['precision']:.4f}")
    print(f"Recall: {results['recall']:.4f}")
    print(f"{'='*50}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_analysis.py <your_csv_file.csv>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    analyze_csv(csv_file)
