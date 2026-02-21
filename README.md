# 🛡️ Gmail Spam Detection Using Machine Learning

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![Machine Learning](https://img.shields.io/badge/Machine_Learning-Scikit_Learn-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Overview
**Gmail Spam Detection Using Machine Learning** is a Python-based Streamlit web application acting as a personal inbox security guard. It detects spam emails in Gmail accounts using a custom Naive Bayes machine learning model.

The system integrates seamlessly with the **Gmail API** for real-time email monitoring and the **VirusTotal API** for enhanced security analysis of attachments and embedded links. Users can analyze individual emails, scan entire inboxes interactively, and generate detailed threat assessment reports.

---

## ✨ Key Features

### 📧 Gmail Integration
- **OAuth 2.0 Authentication:** Secure, direct access to your Gmail inbox.
- **Real-Time Monitoring:** Automatic fetching and parsing of complex MIME email structures.
- **Privacy First:** Strict read-only access ensures your data cannot be altered or deleted.

### 🧠 Spam Detection Pipeline
- **Machine Learning:** Powered by a Naive Bayes classifier trained on natural language email content.
- **Deep Text Analysis:** Evaluates sender context, subject lines, body text, and embedded URLs.
- **Granular Confidence:** Provides exact spam probability percentages rather than just binary outputs.

### 🦠 Security & Threat Analysis
- **VirusTotal API Integration:** Scans extracted attachments and URLs against a database of 70+ antivirus engines.
- **Threat Level Classification:** Real-time assessment categorizing risks as High, Medium, or Low.
- **Memory-Safe Handling:** Downloads and processes attachments securely in memory without saving malicious files to your local disk.

---

## 🏗️ System Architecture

The application is built on a modular architecture, separating the frontend UI, API integrations, and machine learning logic to maintain a clean, scalable codebase.

### Application Flow
```mermaid
graph TD
    UI[🖥️ Streamlit Frontend]
    Gmail[📧 Gmail API]
    ML[🧠 ML Model & Vectorizer]
    VT[🦠 VirusTotal API]

    UI -- "1. OAuth 2.0 Auth" --> Gmail
    Gmail -- "2. Returns Inbox Data" --> UI
    UI -- "3. Sends Email Body Text" --> ML
    ML -- "4. Returns Spam Probability" --> UI
    UI -- "5. Uploads File Bytes & URLs" --> VT
    VT -- "6. Returns Threat Report" --> UI
    graph LR
    A[Raw Email Text] -->|Clean & Format| B(TF-IDF Vectorizer)
    B -->|Numerical Matrix| C(Trained Naive Bayes Model)
    C --> D{Prediction}
    D -->|1| E[🚨 Spam / High Threat]
    D -->|0| F[✅ Clean / Ham]
    📋 Prerequisites

Python: 3.8 or higher

Libraries: pandas, numpy, scikit-learn, streamlit, requests, joblib, beautifulsoup4, python-dotenv, google-api-python-client, google-auth-oauthlib

Credentials:

Gmail API credentials (credentials.json)

VirusTotal API key
⚙️ Installation & Setup

Clone the repository
git clone https://github.com/Allyankhan/SMS-SPAM-DETECTION-USING-MACHINE-LEARNING.git
cd SMS-SPAM-DETECTION-USING-MACHINE-LEARNING
2.Create a virtual environment
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
🔑 API Configuration
Gmail API Setup

Create a project in the Google Cloud Console
.

Enable the Gmail API.

Create OAuth 2.0 credentials and select Desktop App as the application type.

Download the file, rename it to credentials.json, and place it in the project root.

VirusTotal API Setup

Create a free account at VirusTotal
.

Obtain your API key from your profile dashboard.

Create a .env file in the project root and add your key:

VIRUSTOTAL_API_KEY=your_actual_api_key_here
🚀 Usage & Functionalities

Run the application locally:

streamlit run app.py

Open the URL displayed in the terminal (usually http://localhost:8501) and authenticate via the sidebar.

🎛️ Dashboard Tabs

✍️ Manual Entry: Paste raw text or links to instantly classify content and scan URLs without needing an email context.

📧 Single Email: Select a recent email from your inbox. The app extracts the body and attachments, calculates spam probability, and scans files/links via VirusTotal.

📥 Batch Analysis: Fetch multiple emails simultaneously. Processes them in real-time, displays a detailed dataframe, and allows exporting the full security report as a CSV.

💻 Programmatic API Usage

You can also use the core logic outside of Streamlit:

from model_handler import load_ml_assets, predict_spam

model, vectorizer = load_ml_assets()
text = "Congratulations, you won a free iPhone! Click here to claim your prize."

label, probability = predict_spam(text, model, vectorizer)
print(f"Result: {label} (Confidence: {probability}%)")
🔒 Security Notes

Strict Exclusions: Ensure credentials.json, token.json, and .env are listed in .gitignore. Never push these files to a public repository.

Data Privacy: The application uses the gmail.readonly scope only. No emails are permanently stored, modified, or deleted.

👨‍💻 Author

Allyan Nawab Khan
Computer Software Engineering, UET Mardan

📄 License

This project is licensed under the MIT License - see the LICENSE
 file for details.

🙏 Acknowledgements

Built with Streamlit

ML modeling via Scikit-Learn

Security integrations by VirusTotal

Email parsing via Google Workspace APIs