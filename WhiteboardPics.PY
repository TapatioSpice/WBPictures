import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os

# Function to rename images based on your specifications
def rename_images(uploaded_files):
    renamed_files = []
    file_count = len(uploaded_files)
    rename_map = {
        4: ['PV', 'RG', 'LS', 'CUST'],
        7: ['PV1', 'PV2', 'RG1', 'RG2', 'LS1', 'LS2', 'CUST'],
        10: ['PV1', 'PV2', 'PV3', 'RG1', 'RG2', 'RG3', 'LS1', 'LS2', 'LS3', 'CUST']
    }
    rename_prefixes = rename_map[file_count]
    
    for i, file in enumerate(uploaded_files):
        new_filename = rename_prefixes[i] + os.path.splitext(file.name)[1]
        renamed_files.append((file, new_filename))
    return renamed_files

# Function to send email with attachments
def send_email(renamed_files):
    # Email setup
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    sender_email = 'alex@alphalandscapeslv.com'
    password = 'Monster#12!'
    subject = "WB " + datetime.now().strftime("%Y-%m-%d")

    # Create the message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['Subject'] = subject

    # Recipients
    recipients_accounting = "Accounting@alphalandscapeslv.com"
    recipients_cc_accounting = ["Joey@alphalandscapeslv.com", "MariaO@alphalandscapeslv.com", "Michael@alphalandscapeslv.com", "Michelle@alphalandscapeslv.com", "Myranda@alphalandscapeslv.com", "Samantha@alphalandscapeslv.com", "Tracy@alphalandscapeslv.com"]
    recipients_cc_cust = ["Darrell@alphalandscapeslv.com", "Joey@alphalandscapeslv.com", "MariaO@alphalandscapeslv.com", "Tracy@alphalandscapeslv.com", "Will@alphalandscapeslv.com"]

    # Attach files to the email
    for file, new_filename in renamed_files:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.getvalue())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {new_filename}')
        msg.attach(part)

    # Split into two emails if necessary
    msg_to_accounting = msg.copy()
    msg_to_accounting['To'] = recipients_accounting
    msg_to_accounting['Cc'] = ', '.join(recipients_cc_accounting)
    
    msg_to_cust = msg.copy()
    msg_to_cust['To'] = recipients_accounting
    msg_to_cust['Cc'] = ', '.join(recipients_cc_cust)
    
    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        # Send to accounting
        server.sendmail(sender_email, [recipients_accounting] + recipients_cc_accounting, msg_to_accounting.as_string())
        # Send to CUST
        server.sendmail(sender_email, [recipients_accounting] + recipients_cc_cust, msg_to_cust.as_string())

# Streamlit app interface
st.title("Image Renamer & Email Sender")

uploaded_files = st.file_uploader("Upload your images", type=["jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    renamed_files = rename_images(uploaded_files)
    for _, new_filename in renamed_files:
        st.write(f"Renamed to: {new_filename}")
    
    if st.button("Send Email"):
        send_email(renamed_files)
        st.success("Emails sent successfully!")
