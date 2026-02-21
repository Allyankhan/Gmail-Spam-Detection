import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
VT_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
VT_UPLOAD_URL = "https://www.virustotal.com/api/v3/files"
VT_URL_SCAN_URL = "https://www.virustotal.com/api/v3/urls"
VT_ANALYSIS_URL = "https://www.virustotal.com/api/v3/analyses/"

def _poll_analysis(analysis_id, headers):
    """Helper function to wait for VT analysis to complete."""
    for _ in range(6):  # Try 6 times
        time.sleep(5)
        report_url = VT_ANALYSIS_URL + analysis_id
        report_res = requests.get(report_url, headers=headers)
        
        if report_res.status_code == 200:
            data = report_res.json()
            if data.get("data", {}).get("attributes", {}).get("status") == "completed":
                stats = data["data"]["attributes"]["stats"]
                malicious = stats.get("malicious", 0)
                suspicious = stats.get("suspicious", 0)
                
                if malicious > 0:
                    return {"status": "High", "malicious_hits": malicious, "suspicious_hits": suspicious}
                elif suspicious > 0:
                    return {"status": "Medium", "malicious_hits": malicious, "suspicious_hits": suspicious}
                else:
                    return {"status": "Low", "malicious_hits": 0, "suspicious_hits": 0}
                    
    return {"error": "Scan timed out."}

def scan_attachment(file_bytes, filename):
    """Uploads file to VT and waits for the scan report."""
    if not VT_API_KEY: return {"error": "API key missing."}
    headers = {"x-apikey": VT_API_KEY}
    files = {"file": (filename, file_bytes)}

    upload_res = requests.post(VT_UPLOAD_URL, headers=headers, files=files)
    if upload_res.status_code != 200: return {"error": "Upload failed."}
    
    return _poll_analysis(upload_res.json().get("data", {}).get("id"), headers)

def scan_url(url):
    """Submits a URL to VT and waits for the scan report."""
    if not VT_API_KEY: return {"error": "API key missing."}
    headers = {"x-apikey": VT_API_KEY, "accept": "application/json"}
    
    scan_res = requests.post(VT_URL_SCAN_URL, headers=headers, data={"url": url})
    if scan_res.status_code != 200: return {"error": "URL submission failed."}
    
    return _poll_analysis(scan_res.json().get("data", {}).get("id"), headers)