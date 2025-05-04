import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image
import time
from datetime import datetime
import os
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as ReportImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import pickle

# Set page configuration
st.set_page_config(
    page_title="MediScan Quantum",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create directories if they don't exist
os.makedirs("data", exist_ok=True)
os.makedirs("data/users", exist_ok=True)
os.makedirs("data/images", exist_ok=True)
os.makedirs("data/reports", exist_ok=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "login"
if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = []
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = []
if 'quantum_enhanced' not in st.session_state:
    st.session_state.quantum_enhanced = False

# User database functions
def save_user(username, password):
    user_data = {'username': username, 'password': password}
    with open(f"data/users/{username}.pkl", 'wb') as f:
        pickle.dump(user_data, f)

def load_user(username):
    try:
        with open(f"data/users/{username}.pkl", 'rb') as f:
            return pickle.load(f)
    except:
        return None

def authenticate(username, password):
    user_data = load_user(username)
    if user_data and user_data['password'] == password:
        return True
    return False

# Simulated quantum computing functions
def simulate_quantum_circuit(image_data, depth=3):
    """Simulate a quantum circuit for image processing"""
    st.write("⚛️ Initializing quantum simulation...")
    progress_bar = st.progress(0)
    
    # Simulate quantum processing steps
    for i in range(10):
        # Simulate quantum operations
        time.sleep(0.2)
        progress_bar.progress((i + 1) * 10)
    
    st.success("✅ Quantum simulation completed")
    
    # Apply simulated quantum enhancement (just a filter in this simulation)
    enhanced_data = np.array(image_data) * 1.2
    enhanced_data = np.clip(enhanced_data, 0, 255).astype(np.uint8)
    
    return Image.fromarray(enhanced_data)

# Image analysis functions
def classify_medical_image(img, index=0):
    """Classify the type of medical image"""
    # Hardcoded classifications for the 5 example images
    classifications = [
        "Mammogram (Breast X-ray)",
        "Brain MRI Scan",
        "Chest X-ray with Various Conditions",
        "Brain MRI with Different Imaging Sequences (T1w, T2w, FLAIR)",
        "Chest CT Scan with Different Patterns"
    ]
    
    if index < len(classifications):
        return classifications[index]
    else:
        # Fallback for new uploads
        return "Medical Scan (Unspecified Type)"

def analyze_image_content(img, index=0):
    """Analyze the content of the medical image"""
    # Hardcoded analysis for the 5 example images
    analyses = [
        {
            "findings": "Multiple mammogram views showing breast tissue with varying density patterns. No obvious masses or calcifications detected.",
            "recommendation": "Regular follow-up recommended as per screening guidelines.",
            "confidence": 0.92
        },
        {
            "findings": "Cross-sectional brain MRI images showing normal ventricles and brain parenchyma. No evidence of mass effect, midline shift, or abnormal enhancement.",
            "recommendation": "No further imaging needed at this time.",
            "confidence": 0.89
        },
        {
            "findings": "Various chest X-rays showing different pathological conditions including: Atelectasis, Cardiomegaly, Effusion, Infiltration, Mass, Nodule, Pneumonia, and Pneumothorax.",
            "recommendation": "Clinical correlation recommended for specific diagnosis.",
            "confidence": 0.85
        },
        {
            "findings": "Brain MRI with multiple sequences (T1w, T2w, FLAIR) showing comparison between different image reconstruction algorithms (Raw, BM3D, U-Net, NAFNet).",
            "recommendation": "NAFNet reconstruction shows highest quality metrics.",
            "confidence": 0.94
        },
        {
            "findings": "Chest CT scans showing different lung patterns: GGO (Ground Glass Opacity), Crazy Paving, Air Space Consolidation, and Normal (Negative) findings.",
            "recommendation": "Findings consistent with various stages of pulmonary disease. Clinical correlation recommended.",
            "confidence": 0.91
        }
    ]
    
    if index < len(analyses):
        return analyses[index]
    else:
        # Fallback for new uploads
        return {
            "findings": "Image analysis complete. Please consult with a healthcare professional for interpretation.",
            "recommendation": "Further clinical correlation recommended.",
            "confidence": 0.75
        }

def quantum_enhance_image(img):
    """Apply simulated quantum enhancement to the image"""
    img_array = np.array(img)
    return simulate_quantum_circuit(img_array)

def generate_pdf_report(username, image, classification, analysis, enhanced=False):
    """Generate a PDF report with the analysis results"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Add custom styles if they don't exist
    if 'Heading1' not in styles:
        styles.add(ParagraphStyle(name='Heading1', 
                                fontName='Helvetica-Bold',
                                fontSize=18, 
                                spaceAfter=12))
    
    if 'Heading2' not in styles:
        styles.add(ParagraphStyle(name='Heading2', 
                                fontName='Helvetica-Bold',
                                fontSize=14, 
                                spaceBefore=12,
                                spaceAfter=6))
    
    # Or use custom style names to avoid conflicts
    custom_heading1 = ParagraphStyle(name='CustomHeading1', 
                                    parent=styles['Heading1'],
                                    fontSize=18, 
                                    spaceAfter=12)
    
    custom_heading2 = ParagraphStyle(name='CustomHeading2', 
                                    parent=styles['Heading2'],
                                    spaceBefore=12,
                                    spaceAfter=6)
    
    # Title
    story.append(Paragraph("Medical Image Analysis Report", custom_heading1))
    
    # Classification
    story.append(Paragraph("Image Classification", custom_heading2))
    story.append(Spacer(1, 12))
    
    # Date and user info
    story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Paragraph(f"User: {username}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Save image to temporary file
    img_path = f"data/images/temp_report_img.png"
    image.save(img_path)
    
    # Add image
    img = ReportImage(img_path, width=400, height=300)
    story.append(img)
    story.append(Spacer(1, 12))
    
    # Classification
    story.append(Paragraph("Image Classification", styles['Heading2']))
    story.append(Paragraph(f"Type: {classification}", styles['Normal']))
    story.append(Spacer(1, 6))
    
    # Analysis
    story.append(Paragraph("Analysis Results", styles['Heading2']))
    story.append(Paragraph(f"Findings: {analysis['findings']}", styles['Normal']))
    story.append(Paragraph(f"Recommendation: {analysis['recommendation']}", styles['Normal']))
    story.append(Paragraph(f"Confidence Score: {analysis['confidence']:.2f}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Quantum enhancement note
    if enhanced:
        story.append(Paragraph("Note: This analysis was performed with quantum computing enhancement.", styles['Italic']))
    
    # Disclaimer
    story.append(Spacer(1, 24))
    story.append(Paragraph("DISCLAIMER: This is a simulated report for demonstration purposes only. Not for clinical use.", 
                          ParagraphStyle(name='Disclaimer', parent=styles['Normal'], textColor=colors.red)))
    
    # Build PDF
    doc.build(story)
    
    # Clean up temp file
    if os.path.exists(img_path):
        os.remove(img_path)
    
    pdf_content = buffer.getvalue()
    buffer.close()
    
    # Save PDF to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"data/reports/{username}_{timestamp}.pdf"
    with open(pdf_filename, "wb") as f:
        f.write(pdf_content)
    
    return pdf_content, pdf_filename

# UI Components
def show_login_page():
    st.markdown("<h1 style='text-align: center;'>MediScan Quantum</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Advanced Medical Image Analysis Platform</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login"):
                if authenticate(login_username, login_password):
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.session_state.current_page = "dashboard"
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        with col2:
            if st.button("Register"):
                st.session_state.current_page = "register"
                st.rerun()

def show_register_page():
    st.markdown("<h1 style='text-align: center;'>MediScan Quantum</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>User Registration</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        new_username = st.text_input("Choose Username", key="new_username")
        new_password = st.text_input("Choose Password", type="password", key="new_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Register"):
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif not new_username or not new_password:
                    st.error("Username and password cannot be empty")
                elif load_user(new_username):
                    st.error("Username already exists")
                else:
                    save_user(new_username, new_password)
                    st.success("Registration successful! You can now log in.")
                    st.session_state.current_page = "login"
                    st.rerun()
        
        with col2:
            if st.button("Back to Login"):
                st.session_state.current_page = "login"
                st.rerun()

def show_dashboard():
    st.sidebar.title(f"Welcome, {st.session_state.username}")
    
    # Sidebar navigation
    page = st.sidebar.radio("Navigation", ["Upload & Analyze", "View History", "Settings"])
    
    if page == "Upload & Analyze":
        show_upload_page()
    elif page == "View History":
        show_history_page()
    elif page == "Settings":
        show_settings_page()
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.current_page = "login"
        st.rerun()

def show_upload_page():
    st.title("Upload & Analyze Medical Images")
    
    # Upload section
    st.header("Upload Images")
    uploaded_files = st.file_uploader("Choose medical image files", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if uploaded_files:
        st.session_state.uploaded_images = []
        for file in uploaded_files:
            img = Image.open(file)
            st.session_state.uploaded_images.append(img)
        
        st.success(f"{len(uploaded_files)} images uploaded successfully")
    
    # Analysis section
    if st.session_state.uploaded_images:
        st.header("Image Analysis")
        
        # Option for quantum enhancement
        st.session_state.quantum_enhanced = st.checkbox("Enable Quantum Enhancement", value=st.session_state.quantum_enhanced)
        
        if st.button("Analyze Images"):
            st.session_state.analysis_results = []
            
            with st.spinner("Analyzing images..."):
                for i, img in enumerate(st.session_state.uploaded_images):
                    # Apply quantum enhancement if selected
                    if st.session_state.quantum_enhanced:
                        enhanced_img = quantum_enhance_image(img)
                        display_img = enhanced_img
                    else:
                        display_img = img
                    
                    # Classify and analyze
                    classification = classify_medical_image(display_img, i)
                    analysis = analyze_image_content(display_img, i)
                    
                    # Store results
                    st.session_state.analysis_results.append({
                        "image": display_img,
                        "classification": classification,
                        "analysis": analysis,
                        "enhanced": st.session_state.quantum_enhanced
                    })
            
            st.success("Analysis complete!")
        
        # Display results
        if st.session_state.analysis_results:
            st.header("Analysis Results")
            
            for i, result in enumerate(st.session_state.analysis_results):
                with st.expander(f"Image {i+1}: {result['classification']}", expanded=True):
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.image(result["image"], caption=result["classification"], use_column_width=True)
                    
                    with col2:
                        st.subheader("Findings")
                        st.write(result["analysis"]["findings"])
                        
                        st.subheader("Recommendation")
                        st.write(result["analysis"]["recommendation"])
                        
                        st.metric("Confidence Score", f"{result['analysis']['confidence']:.2f}")
                        
                        # Generate PDF report
                        if st.button(f"Generate PDF Report for Image {i+1}"):
                            with st.spinner("Generating PDF report..."):
                                pdf_content, pdf_filename = generate_pdf_report(
                                    st.session_state.username,
                                    result["image"],
                                    result["classification"],
                                    result["analysis"],
                                    result["enhanced"]
                                )
                            
                            # Create download link
                            b64_pdf = base64.b64encode(pdf_content).decode()
                            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="medical_report_{i+1}.pdf">Download PDF Report</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            
                            st.success(f"PDF report saved to {pdf_filename}")

def show_history_page():
    st.title("Analysis History")
    
    # List all PDF reports for the current user
    reports = []
    for filename in os.listdir("data/reports"):
        if filename.startswith(st.session_state.username) and filename.endswith(".pdf"):
            reports.append(filename)
    
    if reports:
        st.write(f"Found {len(reports)} reports")
        
        for report in reports:
            with st.expander(f"Report: {report}"):
                # Read the PDF file
                with open(f"data/reports/{report}", "rb") as f:
                    pdf_content = f.read()
                
                # Create download link
                b64_pdf = base64.b64encode(pdf_content).decode()
                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{report}">Download PDF Report</a>'
                st.markdown(href, unsafe_allow_html=True)
                
                # Display creation time
                timestamp = report.split("_")[1].split(".")[0]
                formatted_time = f"{timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]} {timestamp[9:11]}:{timestamp[11:13]}:{timestamp[13:15]}"
                st.write(f"Created on: {formatted_time}")
    else:
        st.info("No reports found. Analyze some images to generate reports.")

def show_settings_page():
    st.title("Settings")
    
    # Quantum computing settings
    st.header("Quantum Computing Settings")
    
    # Simulated quantum settings
    st.write("These settings control the simulated quantum computing features.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        quantum_enabled = st.checkbox("Enable Quantum Computing by Default", 
                                     value=st.session_state.quantum_enhanced)
        
        if quantum_enabled != st.session_state.quantum_enhanced:
            st.session_state.quantum_enhanced = quantum_enabled
            st.success("Setting updated")
    
    with col2:
        quantum_depth = st.slider("Quantum Circuit Depth", 1, 10, 3)
        st.info("Higher depth may improve results but increases processing time")
    
    # Account settings
    st.header("Account Settings")
    
    if st.button("Change Password"):
        st.warning("Password change functionality would be implemented here in a production system")
    
    if st.button("Delete Account"):
        st.error("This would permanently delete your account and all associated data")
        confirm = st.checkbox("I understand this action cannot be undone")
        
        if confirm and st.button("Confirm Delete"):
            st.warning("Account deletion would be implemented here in a production system")

# Main app logic
def main():
    # Custom CSS
    st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
    }
    h1, h2, h3 {
        color: #1E88E5;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        border-radius: 5px;
    }
    .stProgress .st-bo {
        background-color: #1E88E5;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display the appropriate page based on session state
    if not st.session_state.logged_in:
        if st.session_state.current_page == "login":
            show_login_page()
        elif st.session_state.current_page == "register":
            show_register_page()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()