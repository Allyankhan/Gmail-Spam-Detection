Gmail Spam Detection Using Machine Learning (Streamlit App)
Overview

Gmail Spam Detection Using Machine Learning is a Python-based Streamlit web application that detects spam emails in Gmail accounts using a Naive Bayes machine learning model. The system integrates with the Gmail API for real-time email monitoring and VirusTotal API for enhanced security analysis of attachments and links.

It allows users to analyze individual emails or entire inboxes interactively, providing spam classification, threat assessment, and detailed security reports.

Key Features
Gmail Integration

Direct access to Gmail inbox via OAuth 2.0 authentication

Real-time email monitoring and automatic fetching

Read-only access ensures privacy and security

Spam Detection

Naive Bayes classifier trained on email content

Analyzes sender, subject, body text, and links

Provides spam probability and classification

Security Analysis

VirusTotal API integration for attachment and link scanning

Real-time threat assessment using multiple antivirus engines

Suspicious pattern detection and threat-level classification

Secure handling of attachments and tokens

User Interface

Interactive Streamlit web application

Real-time email analysis results

Detailed security reports with visual threat indicators

Single email and batch email classification

Prerequisites

Python 3.x

Required Python packages (install via requirements.txt):

pandas, numpy, scikit-learn, streamlit, requests, pickle

Gmail API credentials (credentials.json)

VirusTotal API key (for attachment/link analysis)

Project Structure
Gmail-SPAM-DETECTION/
├── app.py                 # Streamlit web application
├── credentials.json       # Gmail API credentials (local only)
├── gmail_api.py           # Gmail API integration
├── model_handler.py       # Naive Bayes model and prediction logic
├── model.pkl              # Trained Naive Bayes model
├── vectorizer.pkl         # TF-IDF vectorizer for text preprocessing
├── vt_api.py              # VirusTotal API helper
├── token.json             # Gmail OAuth token (local only)
├── .env                   # Environment variables (VIRUSTOTAL_API_KEY)
├── requirements.txt       # Python dependencies
└── .gitignore             # Ignore sensitive files
Installation

Clone the repository

git clone https://github.com/Allyankhan/Gmail-Spam-Detection.git
cd Gmail-SPAM-DETECTION

Create a virtual environment

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

Install dependencies

pip install -r requirements.txt

Gmail API Setup

Create a project in Google Cloud Console

Enable Gmail API and create OAuth 2.0 credentials

Save credentials.json in the project root

First run generates token.json (store locally; do not push to GitHub)

VirusTotal API Setup

Get an API key from VirusTotal

Set it in .env or environment variable:

export VIRUSTOTAL_API_KEY="your_api_key"   # Linux/Mac
set VIRUSTOTAL_API_KEY="your_api_key"      # Windows
Usage
Run the Streamlit App
streamlit run app.py

Open the URL displayed in the terminal (usually http://localhost:8501)

Authenticate Gmail when prompted

Functionalities

Single Email Analysis

Enter email content manually or select from Gmail inbox

Classifies email as Spam or Ham using Naive Bayes

Shows spam probability

Batch Email Analysis

Fetches multiple emails from Gmail inbox

Classifies them in real time

Saves results to CSV (optional)

Attachment/Link Security

VirusTotal scans for attachments and URLs

Threat levels classified as High / Medium / Low

Visual indicators for suspicious files

Python API Example
Single Email Classification
from model_handler import load_model, predict_email

# Load model and vectorizer
model, vectorizer = load_model()

email = {
    "sender": "example@domain.com",
    "subject": "Win a prize!",
    "body": "Congratulations, you won...",
    "urls": ["http://suspicious-link.com"]
}

prediction = predict_email(email, model, vectorizer)
print(f"Prediction: {prediction}")
Batch Email Classification
import pandas as pd
from model_handler import load_model, batch_predict

model, vectorizer = load_model()
emails_df = pd.read_csv("emails.csv")
predictions = batch_predict(emails_df, model, vectorizer)
emails_df["predicted_label"] = predictions
emails_df.to_csv("emails_with_predictions.csv", index=False)
Security Notes

Never push credentials.json, token.json, or API keys to GitHub

All sensitive credentials should be local or in .env

Gmail API access is read-only, and emails are not stored in the repo

Contributing

Fork the repository

Create a new branch: git checkout -b feature/your-feature

Commit your changes: git commit -m "Add feature"

Push your branch: git push origin feature/your-feature

Open a Pull Request

License

MIT License – see LICENSE
 for details

Acknowledgements

Gmail API
 for email access

VirusTotal API
 for attachment/link scanning

Streamlit
 for interactive UI

NLTK
 and Scikit-learn
 for ML and NLP

