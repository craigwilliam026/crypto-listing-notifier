import smtplib
from email.mime.text import MIMEText
import os

# Email credentials for Outlook/Hotmail
smtp_server = 'smtp-mail.outlook.com'
smtp_port = 587
email_user = os.getenv('EMAIL_USER')  # Ensure these are set in your GitHub secrets
email_password = os.getenv('EMAIL_PASSWORD')
recipient_email = 'lelouch0zerogeass@gmail.com'

def send_test_email(subject, body):
    print("Preparing to send test email...")
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = recipient_email
    
    try:
        print("Connecting to SMTP server...")
        with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
            server.set_debuglevel(1)  # Enable debug output for SMTP
            print("Starting TLS...")
            server.starttls()
            print("TLS started")
            print("Logging in to SMTP server...")
            server.login(email_user, email_password)
            print("Logged in successfully")
            print("Sending email...")
            server.sendmail(email_user, recipient_email, msg.as_string())
            print("Test email sent successfully")
    except Exception as e:
        print(f"Error sending test email: {e}")

# Test email content
subject = "Test Email"
body = "This is a test email to verify the email functionality."

send_test_email(subject, body)
