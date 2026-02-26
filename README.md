\documentclass[11pt,a4paper]{article}

\usepackage[margin=1in]{geometry}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{titlesec}

\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    urlcolor=blue
}

\titleformat{\section}{\large\bfseries}{}{0em}{}
\titleformat{\subsection}{\normalsize\bfseries}{}{0em}{}

\title{\textbf{Gmail-Spam-Detection\_Using-Machine\_Learning} \\[6pt]
\large Machine Learning–Based Gmail Spam Detection \& Threat Intelligence System}

\author{}
\date{}

\begin{document}

\maketitle
\hrule
\vspace{0.5cm}

\section*{Project Overview}

This project is an end-to-end spam detection and threat intelligence system that integrates directly with Gmail using OAuth 2.0 authentication. It automatically monitors incoming emails, classifies them using a Machine Learning model, and performs malicious URL and attachment scanning via the VirusTotal API.

The system combines \textbf{Machine Learning, Cybersecurity, and Cloud API Integration} into a production-ready Python application.

\section*{System Architecture}

\subsection*{Secure Gmail Integration}
\begin{itemize}[leftmargin=*]
    \item OAuth 2.0 authentication
    \item Real-time inbox access via Gmail API
    \item Automated fetching of new emails
\end{itemize}

\subsection*{Machine Learning Pipeline}
\begin{itemize}[leftmargin=*]
    \item Text preprocessing and cleaning
    \item TF-IDF vectorization
    \item Multinomial Naive Bayes classifier
    \item Probability-based scoring for interpretability
\end{itemize}

\subsection*{Threat Intelligence Layer}
\begin{itemize}[leftmargin=*]
    \item VirusTotal API integration
    \item Malicious URL detection
    \item Suspicious attachment scanning
    \item Real-time threat analysis
\end{itemize}

\subsection*{Interactive Dashboard}
\begin{itemize}[leftmargin=*]
    \item Built with Streamlit
    \item Live spam prediction results
    \item Threat detection insights
    \item Email risk scoring visualization
\end{itemize}

\section*{Tech Stack}

\begin{itemize}[leftmargin=*]
    \item Python
    \item Scikit-learn
    \item Streamlit
    \item Gmail API
    \item VirusTotal API
\end{itemize}

\section*{How It Works}

\begin{enumerate}[leftmargin=*]
    \item User authenticates securely via Gmail OAuth 2.0
    \item System fetches new emails in real time
    \item Email text is preprocessed and vectorized using TF-IDF
    \item Multinomial Naive Bayes predicts spam probability
    \item URLs and attachments are scanned using VirusTotal
    \item Results are displayed on an interactive dashboard
\end{enumerate}

\section*{Model Details}

\begin{itemize}[leftmargin=*]
    \item \textbf{Algorithm:} Multinomial Naive Bayes
    \item \textbf{Vectorization:} TF-IDF
    \item \textbf{Feature Type:} Email text content
    \item \textbf{Output:} Spam probability score
\end{itemize}

\section*{Project Structure}

\begin{verbatim}
├── app.py
├── credentials.json
├── gmail_api.py
├── model_handler.py
├── requirements.txt
├── model.pkl
├── vectorizer.pkl
├── vt_api.py
└── README.md
\end{verbatim}

\section*{What This Project Demonstrates}

\begin{itemize}[leftmargin=*]
    \item End-to-end ML pipeline development
    \item Secure OAuth-based Gmail integration
    \item Real-time email monitoring architecture
    \item Combining machine learning with cybersecurity workflows
    \item Modular and scalable Python application design
\end{itemize}

\section*{Future Improvements}

\begin{itemize}[leftmargin=*]
    \item Deep Learning-based spam classifier (LSTM / BERT)
    \item Email phishing detection model
    \item Cloud deployment (AWS / GCP / Azure)
    \item Docker containerization
    \item Admin monitoring dashboard
    \item Automated model retraining pipeline
\end{itemize}

\section*{License}

This project is licensed under the MIT License.

\vspace{1cm}
\hrule
\vspace{0.3cm}
\centerline{\textit{Built with Machine Learning + Cybersecurity + Cloud Integration}}

\end{document}
