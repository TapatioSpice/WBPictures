import streamlit as st
import os
import smtplib
from email.message import EmailMessage
from typing import List, Tuple

# Function to rename files
def rename_files(files: List[Tuple[str, str]]):
    for old_name, new_name in files:
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
        else:
            st.error(f"File not found: {old_name}")

# Function to send emails
def send_email(renamed_files: List[str]):
    sender_email = "your_email@example.com"
    sender_password = "your_password"
    recipient_email = "recipient@example.com"

    # Setup email server
    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    for file in renamed_files:
        msg = EmailMessage()
        msg.set_content("Attached is the file you requested.")
        msg['Subject'] = 'File Attachment'
        msg['From'] = sender_email
        msg['To'] = recipient_email

        with open(file, 'rb') as f:
            file_content = f.read()
            msg.add_attachment(file_content, maintype='application', subtype='octet-stream', filename=os.path.basename(file))

        server.send_message(msg)
    
    server.quit()

# Streamlit app
def main():
    st.title("File Upload and Rename App")

    uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)

    if uploaded_files:
        save_directory = "./uploaded_files"
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        
        file_paths = []
        for uploaded_file in uploaded_files:
            file_path = os.path.join(save_directory, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            file_paths.append(file_path)

        st.write("Files uploaded:")
        st.write(file_paths)

        # Rename files - example renaming logic
        renamed_files = [(path, os.path.join(save_directory, "new_" + os.path.basename(path))) for path in file_paths]
        rename_files(renamed_files)

        st.write("Renamed files:")
        st.write([new_name for old_name, new_name in renamed_files])

        if st.button("Send Email"):
            send_email([new_name for old_name, new_name in renamed_files])
            st.success("Emails sent successfully!")

if __name__ == "__main__":
    main()
