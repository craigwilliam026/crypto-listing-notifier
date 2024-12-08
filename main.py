import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os

# Email credentials for ProtonMail
smtp_server = 'smtp.protonmail.com'
smtp_port = 587
email_user = os.getenv('EMAIL_USER')  # Make sure to set these as secrets in GitHub
email_password = os.getenv('EMAIL_PASSWORD')
recipient_email = 'lelouch0zerogeass@gmail.com'

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = recipient_email
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.sendmail(email_user, recipient_email, msg.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

def get_upcoming_listings(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        patterns = ["will be listed on", "new listing", "upcoming listing"]
        listings = soup.find_all('div', class_='announcement')
        
        for listing in listings:
            for pattern in patterns:
                if pattern in listing.text.lower():
                    # Extract and parse the date from the listing text
                    # Assuming the date format as YYYY-MM-DD for this example
                    date_str = '2024-12-08'  # Placeholder: extract actual date from listing.text
                    listing_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    
                    if listing_date >= datetime.now().date():
                        send_email("New Crypto Listing Announced", listing.text.strip())
                    break
        print(f"Checked listings for {url}")
    except Exception as e:
        print(f"Error checking listings for {url}: {e}")

# Example URLs (replace with actual URLs of the announcement pages)
urls = [
    'https://www.kucoin.com/announcement/new-listings',
    'https://www.okx.com/help/section/announcements-new-listings',
    'https://www.binance.com/en/support/announcement/new-cryptocurrency-listing?c=48&navId=48',
    'https://announcements.bybit.com/en/?category=new_crypto&page=1',
    'https://www.bitget.com/support/sections/5955813039257',
    'https://www.gate.io/announcements',
    'https://support.bitmart.com/hc/en-us/sections/360000908874-New-Listings'
]

for url in urls:
    get_upcoming_listings(url)
