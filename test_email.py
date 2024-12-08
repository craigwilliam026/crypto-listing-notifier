import smtplib
from email.mime.text import MIMEText
import os

# Email credentials for ProtonMail
smtp_server = 'smtp.protonmail.com'
smtp_port = 587
email_user = os.getenv('EMAIL_USER')  # Ensure these are set in your environment or GitHub secrets
email_password = os.getenv('EMAIL_PASSWORD')
recipient_email = 'lelouch0zerogeass@gmail.com'

def send_test_email(subject, body):
    print("Preparing to send test email...")
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = recipient_email
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.sendmail(email_user, recipient_email, msg.as_string())
        print("Test email sent successfully")
    except Exception as e:
        print(f"Error sending test email: {e}")

# Test email content
subject = "Test Email"
body = "This is a test email to verify the email functionality."

send_test_email(subject, body)
