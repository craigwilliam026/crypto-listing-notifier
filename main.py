import tweepy
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# Twitter API credentials
consumer_key = 'GyWwycS6U8pk2VvwPwr0itsa1'
consumer_secret = 'mr5yvX4k7bmhCxeQHtxPVjyasQaMeVdgOIO5h2lnV1RWUPxNkx'
access_token = '1495991855032713219-ePsJArOAdzD5rvCl4C43CZGrtwTVvi'
access_token_secret = 'kLnAqAhS9r96neMLAOSDG6cynjDENMrKwJsFK5j4nNQR6'

# Email credentials for ProtonMail
smtp_server = 'smtp.protonmail.com'
smtp_port = 587
email_user = 'craigwilliam026@protonmail.com'
email_password = 'craigwilliam026'
recipient_email = 'lelouch0zerogeass@gmail.com'

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = recipient_email
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, recipient_email, msg.as_string())

def check_twitter_announcements():
    exchanges = ["Binance", "Coinbase", "Kraken", "Bithumb", "Bitfinex", "KuCoin", "OKX", "Gate.io", "Bybit",
                 "Bitget", "MEXC", "HTX", "BingX", "Crypto.com", "BitMart", "LBank", "XT.com", "AscendEX",
                 "CoinW", "Weex", "Toobit", "DigiFinex", "P2B", "KCEX", "Bvow", "FameEX", "OrangeX",
                 "WhiteBIT", "HBIT", "Tapbit", "Azbit", "LATOKEN", "Ourbit", "BigONE", "BioFin", "Bika"]
    query = " OR ".join([f'"{exchange} will list" OR "{exchange} to list"' for exchange in exchanges])
    
    for tweet in api.search(q=query, count=100):
        send_email("New Crypto Listing Announced", tweet.text)

def get_upcoming_listings(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    patterns = ["will be listed on", "new listing", "upcoming listing"]
    
    listings = soup.find_all('div', class_='announcement')
    
    for listing in listings:
        for pattern in patterns:
            if pattern in listing.text.lower():
                send_email("New Crypto Listing Announced", listing.text.strip())
                break

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

check_twitter_announcements()
for url in urls:
    get_upcoming_listings(url)
