import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
VT_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
VT_UPLOAD_URL = "https://www.virustotal.com/api/v3/files"
VT_ANALYSIS_URL = "https://www.virustotal.com/api/v3/analyses/"

def scan_attachment(file_bytes, filename):
    """Uploads file to VT and waits for the scan report."""
    if not VT_API_KEY:
        return {"error": "VirusTotal API key missing in .env file."}

    headers = {"x-apikey": VT_API_KEY}
    files = {"file": (filename, file_bytes)}

    # Step 1: Upload the file
    upload_res = requests.post(VT_UPLOAD_URL, headers=headers, files=files)
    if upload_res.status_code != 200:
        return {"error": f"Upload failed: {upload_res.text}"}
    
    analysis_id = upload_res.json().get("data", {}).get("id")
    
    # Step 2: Poll for results (VT needs a moment to analyze)
    for _ in range(5):  # Try 5 times
        time.sleep(5) # Wait 5 seconds between checks
        report_url = VT_ANALYSIS_URL + analysis_id
        report_res = requests.get(report_url, headers=headers)
        
        if report_res.status_code == 200:
            data = report_res.json()
            status = data.get("data", {}).get("attributes", {}).get("status")
            if status == "completed":
                stats = data["data"]["attributes"]["stats"]
                malicious = stats.get("malicious", 0)
                suspicious = stats.get("suspicious", 0)
                
                if malicious > 0 or suspicious > 0:
                    return {"status": "Suspicious", "malicious_hits": malicious, "suspicious_hits": suspicious}
                else:
                    return {"status": "Clean", "malicious_hits": 0, "suspicious_hits": 0}
                    
    return {"error": "Scan timed out. Try again later."}