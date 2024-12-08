import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os
import time
import random

# Email credentials for ProtonMail
smtp_server = 'smtp.protonmail.com'
smtp_port = 587
email_user = os.getenv('EMAIL_USER')  # Make sure to set these as secrets in GitHub
email_password = os.getenv('EMAIL_PASSWORD')
recipient_email = 'lelouch0zerogeass@gmail.com'

# User-Agent headers list
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
]

def send_email(subject, body):
    print("Preparing to send email...")
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
    print(f"Checking listings for {url}...")
    start_time = time.time()
    try:
        headers = {'User-Agent': random.choice(user_agents)}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        patterns = ["will be listed on", "new listing", "upcoming listing"]
        listings = soup.find_all('div', class_='announcement')
        
        for listing in listings:
            for pattern in patterns:
                if pattern in listing.text.lower():
                    # Extract and parse the date from the listing text
                    date_str = '2024-12-08'  # Placeholder: extract actual date from listing.text
                    listing_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    
                    if listing_date >= datetime.now().date():
                        print("New listing found, preparing to send email.")
                        send_email("New Crypto Listing Announced", listing.text.strip())
                    break
        print(f"Completed checking listings for {url} in {time.time() - start_time:.2f} seconds")
        time.sleep(random.uniform(1, 5))  # Random delay between 1 to 5 seconds
    except Exception as e:
        print(f"Error checking listings for {url}: {e}")

def check_twitter_announcements():
    start_time = time.time()
    exchanges = ["Binance", "Coinbase", "Kraken", "Bithumb", "Bitfinex", "KuCoin", "OKX", "Gate.io", "Bybit",
                 "Bitget", "MEXC", "HTX", "BingX", "Crypto.com", "BitMart", "LBank", "XT.com", "AscendEX",
                 "CoinW", "Weex", "Toobit", "DigiFinex", "P2B", "KCEX", "Bvow", "FameEX", "OrangeX",
                 "WhiteBIT", "HBIT", "Tapbit", "Azbit", "LATOKEN", "Ourbit", "BigONE", "BioFin", "Bika"]
    queries = [f'"{exchange} will list" OR "{exchange} to list"' for exchange in exchanges]
    
    for query in queries:
        try:
            headers = {'User-Agent': random.choice(user_agents)}
            url = f"https://twitter.com/search?q={query}&f=live"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            tweets = soup.find_all('div', {'data-testid': 'tweet'})
            
            for tweet in tweets:
                tweet_date = tweet.find('time')['datetime']
                tweet_text = tweet.find('div', {'lang': True}).text
                
                tweet_datetime = datetime.fromisoformat(tweet_date[:-1])
                if tweet_datetime.date() >= datetime.now().date():
                    print("New tweet found, preparing to send email.")
                    send_email("New Crypto Listing Announced", tweet_text)
            print(f"Checked Twitter for query: {query}")
            time.sleep(random.uniform(1, 5))  # Random delay between 1 to 5 seconds
        except Exception as e:
            print(f"Error checking Twitter for query {query}: {e}")
    print(f"Completed checking Twitter announcements in {time.time() - start_time:.2f} seconds")

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

print("Starting Twitter announcements check...")
check_twitter_announcements()
for url in urls:
    get_upcoming_listings(url)
print("Finished checking all sources.")
