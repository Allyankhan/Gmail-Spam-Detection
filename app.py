import streamlit as st
from gmail_api import authenticate_gmail, get_recent_emails, extract_email_data, download_attachment
from vt_api import scan_attachment
from model_handler import load_ml_assets, predict_spam

# Page Config
st.set_page_config(page_title="Email Threat Analyzer", page_icon="🛡️", layout="wide")

st.title("🛡️ Advanced Email & Spam Analyzer")
st.markdown("Authenticate with Gmail to analyze your inbox for spam, phishing, and malicious attachments.")

# Load ML Model
@st.cache_resource
def init_model():
    return load_ml_assets()

try:
    model, vectorizer = init_model()
except Exception as e:
    st.error(f"Failed to load ML models: {e}")
    st.stop()

# Session State for Authentication
if 'gmail_service' not in st.session_state:
    st.session_state.gmail_service = None

# Sidebar Authentication
with st.sidebar:
    st.header("Settings & Auth")
    if st.button("Authenticate Gmail"):
        try:
            with st.spinner("Opening browser for Google Authentication..."):
                service = authenticate_gmail()
                st.session_state.gmail_service = service
            st.success("Successfully authenticated!")
        except Exception as e:
            st.error(f"Authentication failed: {e}")

# Main Logic
if st.session_state.gmail_service:
    service = st.session_state.gmail_service
    
    st.subheader("📬 Recent Emails")
    
    with st.spinner("Fetching emails..."):
        try:
            emails = get_recent_emails(service, max_results=10)
        except Exception as e:
            st.error(f"Could not fetch emails: {e}")
            emails = []
            
    if emails:
        # Create a dictionary for the selectbox to show clean formatting
        email_dict = {f"{em['date'][:10]} | {em['sender']} | {em['subject'][:30]}...": em for em in emails}
        
        selected_email_key = st.selectbox("Select an email to analyze:", list(email_dict.keys()))
        selected_email = email_dict[selected_email_key]
        
        if st.button("Analyze Email", type="primary"):
            st.markdown("---")
            st.subheader("Email Analysis Results")
            
            # Display Metadata
            st.write(f"**Sender:** {selected_email['sender']}")
            st.write(f"**Subject:** {selected_email['subject']}")
            st.write(f"**Date:** {selected_email['date']}")
            
            # Extract Body and Attachments
            with st.spinner("Extracting content..."):
                body, attachments = extract_email_data(service, selected_email['payload'], selected_email['id'])
            
            # Machine Learning Content Analysis
            spam_prediction = predict_spam(body, model, vectorizer)
            
            # Threat Assessment Display
            st.markdown("### Threat Assessment")
            col1, col2, col3 = st.columns(3)
            
            is_high_threat = spam_prediction == "Spam"
            col1.metric("Text Spam Level", spam_prediction, delta="High" if is_high_threat else "Low", delta_color="inverse")
            col2.metric("Suspicious Patterns", "Detected" if is_high_threat else "None")
            col3.metric("Attachments", len(attachments))
            
            # Attachment Analysis
            st.markdown("### Attachment Analysis")
            if attachments:
                for att in attachments:
                    with st.spinner(f"Scanning {att['filename']} with VirusTotal..."):
                        file_bytes = download_attachment(service, att['messageId'], att['attachmentId'])
                        scan_result = scan_attachment(file_bytes, att['filename'])
                        
                        if "error" in scan_result:
                            st.warning(f"- **{att['filename']}**: {scan_result['error']}")
                        else:
                            status_color = "red" if scan_result['status'] == 'Suspicious' else "green"
                            st.markdown(f"- **{att['filename']}**: :{status_color}[{scan_result['status']}] (Malicious hits: {scan_result['malicious_hits']})")
            else:
                st.info("No attachments found in this email.")
                
            # Recommended Action
            st.markdown("### Recommended Action")
            if spam_prediction == "Spam" or any(scan_result.get('status') == 'Suspicious' for att in attachments):
                st.error("🚨 **DO NOT CLICK LINKS OR OPEN ATTACHMENTS.** Delete this email immediately.")
            else:
                st.success("✅ This email appears safe, but always exercise caution with unknown senders.")
                
else:
    st.info("Please authenticate using the sidebar to view and analyze your emails.")