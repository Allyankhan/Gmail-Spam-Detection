📧 Gmail-Spam-Detection_Using-Machine_Learning

Machine Learning–Based Gmail Spam Detection & Threat Intelligence System
A real-time spam detection system that securely connects to your Gmail inbox, analyzes incoming emails using machine learning, and performs advanced malicious activity checks.

🚀 Project Overview

This project is an end-to-end spam detection and threat intelligence system that integrates directly with Gmail using OAuth 2.0 authentication. It automatically monitors incoming emails, classifies them using a Machine Learning model, and performs malicious URL & attachment scanning via VirusTotal.

It combines Machine Learning + Cybersecurity + Cloud API Integration into a production-ready Python application.

🧠 System Architecture
🔐 Secure Gmail Integration

OAuth 2.0 authentication

Real-time inbox access via Gmail API

Automated fetching of new emails

📊 Machine Learning Pipeline

Text preprocessing & cleaning

TF-IDF vectorization

Multinomial Naive Bayes classifier

Probability-based scoring for interpretability

🛡️ Threat Intelligence Layer

VirusTotal API integration

Malicious URL detection

Suspicious attachment scanning

Real-time threat analysis

📈 Interactive Dashboard

Built with Streamlit

Live spam prediction results

Threat detection insights

Email risk scoring visualization

🏗️ Tech Stack

Python

Scikit-learn

Streamlit

Gmail API

VirusTotal API

⚙️ How It Works

🔑 User authenticates securely via Gmail OAuth 2.0

📥 System fetches new emails in real time

🧹 Email text is preprocessed and vectorized (TF-IDF)

🤖 Multinomial Naive Bayes predicts spam probability

🔍 URLs & attachments are scanned using VirusTotal

📊 Results are displayed on an interactive dashboard

📦 Installation
1️⃣ Clone the Repository
git clone https://github.com/Allyankhan/Gmail-Spam-Detection_Using-Machine_Learning.git
cd Gmail-Spam-Detection_Using-Machine_Learning
2️⃣ Create Virtual Environment (Recommended)

python -m venv venv

source venv/bin/activate  # Mac/Linux

venv\Scripts\activate     # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt
🔑 API Configuration
Gmail API Setup

Go to Google Cloud Console

Create a new project

Enable Gmail API

Configure OAuth consent screen

Download credentials.json

Place it in the project root directory

VirusTotal API Setup

Create an account at https://www.virustotal.com

Generate your API key

Add your API key to a .env file:

VIRUSTOTAL_API_KEY=your_api_key_here
▶️ Running the Application
streamlit run app.py

The dashboard will open in your browser automatically.

📊 Model Details

Algorithm: Multinomial Naive Bayes

Vectorization: TF-IDF

Feature Type: Email text content

Output: Spam probability score (interpretable classification)

🧩 Key Features

✔ Secure OAuth-based Gmail integration
✔ Real-time email monitoring
✔ ML-powered spam classification
✔ Probability-based risk scoring
✔ URL & attachment threat detection
✔ Interactive visualization dashboard
✔ Modular and production-ready code structure

🛠️ Project Structure (Example)
├── app.py
├── credentials.json
│── gmail_api.py 
│── model_handler.py   
│── reuirements.txt
|── model.pkl
│── vectorizer.pkl
├── vt_api.py
│── README.md  

🎯 What This Project Demonstrates

✅ End-to-end ML pipeline development

✅ Secure OAuth-based Gmail integration

✅ Real-time email monitoring architecture

✅ Combining machine learning with cybersecurity workflows

✅ Modular, scalable Python application design

🔮 Future Improvements

 Deep Learning-based spam classifier (LSTM / BERT)

 Email phishing detection model

 Deployment on cloud (AWS / GCP / Azure)

 Docker containerization

 Admin monitoring dashboard

 Automated model retraining pipeline

🤝 Contributing

Contributions are welcome!

Fork the repository

Create a feature branch

Commit your changes

Push to your branch

Open a Pull Request

📄 License

This project is licensed under the MIT License.
See the LICENSE file for details.

⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub!
