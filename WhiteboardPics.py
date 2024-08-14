import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

def rename_files(files):
    """Rename the files based on the number of files provided."""
    num_files = len(files)
    renamed_files = []

    if num_files == 4:
        new_names = ['PV.jpg', 'RG.jpg', 'LS.jpg', 'CUST.jpg']
    elif num_files == 7:
        new_names = ['PV1.jpg', 'PV2.jpg', 'RG1.jpg', 'RG2.jpg', 'LS1.jpg', 'LS2.jpg', 'CUST.jpg']
    elif num_files == 10:
        new_names = ['PV1.jpg', 'PV2.jpg', 'PV3.jpg', 'RG1.jpg', 'RG2.jpg', 'RG3.jpg', 
                     'LS1.jpg', 'LS2.jpg', 'LS3.jpg', 'CUST.jpg']
    else:
        raise ValueError("Unsupported number of files.")

    for old_name, new_name in zip(files, new_names):
        os.rename(old_name, new_name)
        renamed_files.append(new_name)

    return renamed_files

def send_email(renamed_files):
    """Send emails with the renamed files attached."""
    # Email settings
    email_address = 'alex@alphalandscapeslv.com'
    email_password = 'Monster#12!'
    smtp_server = 'smtp.office365.com'
    smtp_port = 587

    # Current date for subject line
    current_date = datetime.now().strftime("%Y-%m-%d")

    # First email to Accounting (PV, RG, LS)
    msg_to_accounting = EmailMessage()
    msg_to_accounting['From'] = email_address
    msg_to_accounting['To'] = 'Accounting@alphalandscapeslv2.com'
    msg_to_accounting['CC'] = 'Joey@alphalandscapeslv2.com, MariaO@alphalandscapeslv2.com, Michael@alphalandscapeslv2.com, Michelle@alphalandscapeslv2.com, Myranda@alphalandscapeslv2.com, Samantha@alphalandscapeslv2.com, Tracy@alphalandscapeslv2.com'
    msg_to_accounting['Subject'] = f'WB {current_date}'
    msg_to_accounting.set_content('Please find the attached files.')

    # Attach files for Accounting
    for file in renamed_files:
        if file.startswith(('PV', 'RG', 'LS')):
            with open(file, 'rb') as f:
                file_data = f.read()
                file_name = file
            msg_to_accounting.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    # Second email for CUST
    msg_to_cust = EmailMessage()
    msg_to_cust['From'] = email_address
    msg_to_cust['To'] = 'Accounting@alphalandscapeslv2.com'
    msg_to_cust['CC'] = 'Darrell@alphalandscapeslv2.com, Joey@alphalandscapeslv2.com, MariaO@alphalandscapeslv2.com, Tracy@alphalandscapeslv2.com, Will@alphalandscapeslv2.com'
    msg_to_cust['Subject'] = f'WB {current_date}'
    msg_to_cust.set_content('Please find the attached files.')

    # Attach the CUST file
    for file in renamed_files:
        if file == 'CUST.jpg':
            with open(file, 'rb') as f:
                file_data = f.read()
                file_name = file
            msg_to_cust.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    # Send emails using SMTP
    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(email_address, email_password)
        smtp.send_message(msg_to_accounting)
        smtp.send_message(msg_to_cust)

if __name__ == '__main__':
    # Example usage
    # Assume you have a list of image files in the current directory
    files = ['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg']  # Replace with your actual file names
    renamed_files = rename_files(files)
    send_email(renamed_files)
