import streamlit as st
import pandas as pd
import re
from gmail_api import authenticate_gmail, get_recent_emails, extract_email_data, download_attachment
from vt_api import scan_attachment, scan_url
from model_handler import load_ml_assets, predict_spam

# Page Config
st.set_page_config(page_title="Advanced Email Analyzer", page_icon="🛡️", layout="wide")
st.title("🛡️ Advanced Email & Threat Analyzer")

# Load ML Model
@st.cache_resource
def init_model():
    return load_ml_assets()

try:
    model, vectorizer = init_model()
except Exception as e:
    st.error(f"Failed to load ML models: {e}")
    st.stop()

# Helpers
def extract_urls(text):
    """Finds all HTTP/HTTPS links in a text block."""
    return re.findall(r'(https?://[^\s]+)', text)

def get_overall_threat(spam_label, vt_results):
    """Calculates overall threat level based on text and VT scans."""
    if any(res.get('status') == 'High' for res in vt_results): return "High"
    if spam_label == "Spam": return "High"
    if any(res.get('status') == 'Medium' for res in vt_results): return "Medium"
    return "Low"

# Session State for Authentication
if 'gmail_service' not in st.session_state:
    st.session_state.gmail_service = None

# Sidebar
with st.sidebar:
    st.header("⚙️ Gmail Auth")
    if st.button("Authenticate Gmail"):
        try:
            with st.spinner("Authenticating..."):
                st.session_state.gmail_service = authenticate_gmail()
            st.success("Authenticated!")
        except Exception as e:
            st.error(f"Auth failed: {e}")

# Main Interface Tabs
tab1, tab2, tab3 = st.tabs([" Manual Entry", " Single Email (Gmail)", " Batch Analysis"])

# ==========================================
# TAB 1: MANUAL ENTRY
# ==========================================
with tab1:
    st.subheader("Analyze Text or Links")
    manual_text = st.text_area("Paste email content or text here:", height=200)
    
    if st.button("Analyze Text", type="primary"):
        if manual_text:
            spam_label, prob = predict_spam(manual_text, model, vectorizer)
            urls = extract_urls(manual_text)
            
            col1, col2 = st.columns(2)
            col1.metric("Spam Classification", spam_label, f"{prob}% Confidence", delta_color="inverse" if spam_label=="Spam" else "normal")
            col2.metric("URLs Detected", len(urls))
            
            if urls:
                st.markdown("### URL Security Scan")
                for url in set(urls): # Scan unique URLs only
                    with st.spinner(f"Scanning {url[:30]}..."):
                        res = scan_url(url)
                        if "error" in res:
                            st.warning(f"{url[:50]}... - {res['error']}")
                        else:
                            color = "red" if res['status'] == "High" else "orange" if res['status'] == "Medium" else "green"
                            st.markdown(f"- {url[:50]}... : :{color}[**{res['status']} Threat**]")
        else:
            st.warning("Please enter some text.")

# ==========================================
# TAB 2: SINGLE GMAIL ANALYSIS
# ==========================================
with tab2:
    if st.session_state.gmail_service:
        service = st.session_state.gmail_service
        
        with st.spinner("Fetching emails..."):
            try:
                emails = get_recent_emails(service, max_results=15)
            except Exception as e:
                st.error("Could not fetch emails."); emails = []
                
        if emails:
            email_dict = {f"{em['date'][:10]} | {em['sender']} | {em['subject'][:30]}...": em for em in emails}
            selected_email_key = st.selectbox("Select an email:", list(email_dict.keys()))
            selected_email = email_dict[selected_email_key]
            
            if st.button("Scan Email"):
                st.markdown("---")
                body, attachments = extract_email_data(service, selected_email['payload'], selected_email['id'])
                spam_label, prob = predict_spam(body, model, vectorizer)
                urls = extract_urls(body)
                
                vt_results = []
                
                # Layout
                st.write(f"**From:** {selected_email['sender']} | **Subject:** {selected_email['subject']}")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Spam Level", spam_label, f"{prob}% prob")
                col2.metric("Attachments", len(attachments))
                col3.metric("Links Found", len(urls))
                
                # Attachment Scan
                if attachments:
                    st.markdown("#### Attachment Scan")
                    for att in attachments:
                        with st.spinner(f"Scanning {att['filename']}..."):
                            file_bytes = download_attachment(service, att['messageId'], att['attachmentId'])
                            res = scan_attachment(file_bytes, att['filename'])
                            vt_results.append(res)
                            color = "red" if res.get('status') == "High" else "green"
                            st.markdown(f"- **{att['filename']}**: :{color}[{res.get('status', 'Error')}]")
                            
                # URL Scan
                if urls:
                    st.markdown("#### URL Scan")
                    for url in set(urls)[:5]: # Limit to 5 to avoid API rate limits
                        with st.spinner("Scanning URL..."):
                            res = scan_url(url)
                            vt_results.append(res)
                            color = "red" if res.get('status') == "High" else "green"
                            st.markdown(f"- {url[:40]}... : :{color}[{res.get('status', 'Error')}]")
                            
                # Final Verdict
                overall = get_overall_threat(spam_label, vt_results)
                color = "red" if overall == "High" else "orange" if overall == "Medium" else "green"
                st.subheader(f"Overall Threat Level: :{color}[{overall}]")

    else:
        st.info("Authenticate Gmail in the sidebar first.")

# ==========================================
# TAB 3: BATCH ANALYSIS & EXPORT
# ==========================================
with tab3:
    if st.session_state.gmail_service:
        batch_size = st.slider("Number of recent emails to process:", 5, 50, 10)
        
        if st.button("Start Batch Processing"):
            service = st.session_state.gmail_service
            batch_data = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            emails = get_recent_emails(service, max_results=batch_size)
            
            for i, em in enumerate(emails):
                status_text.text(f"Processing {i+1}/{len(emails)}: {em['subject'][:30]}...")
                body, attachments = extract_email_data(service, em['payload'], em['id'])
                
                spam_label, prob = predict_spam(body, model, vectorizer)
                
                batch_data.append({
                    "Date": em['date'][:10],
                    "Sender": em['sender'],
                    "Subject": em['subject'],
                    "Prediction": spam_label,
                    "Spam Probability (%)": prob,
                    "Attachments": len(attachments),
                    "URLs found": len(extract_urls(body))
                })
                progress_bar.progress((i + 1) / len(emails))
                
            status_text.text("Batch processing complete!")
            
            # Display DataFrame
            df = pd.DataFrame(batch_data)
            st.dataframe(df, use_container_width=True)
            
            # CSV Download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=" Download Results as CSV",
                data=csv,
                file_name='email_batch_analysis.csv',
                mime='text/csv',
            )
    else:
        st.info("Authenticate Gmail in the sidebar first.")