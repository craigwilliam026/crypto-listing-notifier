import tweepy
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

def check_for_announcements():
    exchanges = ["Binance", "Coinbase", "Kraken", "Bithumb", "Bitfinex", "KuCoin", "OKX", "Gate.io", "Bybit",
                 "Bitget", "MEXC", "HTX", "BingX", "Crypto.com", "BitMart", "LBank", "XT.com", "AscendEX",
                 "CoinW", "Weex", "Toobit", "DigiFinex", "P2B", "KCEX", "Bvow", "FameEX", "OrangeX",
                 "WhiteBIT", "HBIT", "Tapbit", "Azbit", "LATOKEN", "Ourbit", "BigONE", "BioFin", "Bika"]
    query = " OR ".join([f"{exchange} will list" for exchange in exchanges])
    
    for tweet in api.search(q=query, count=100):
        send_email("New Crypto Listing Announced", tweet.text)

check_for_announcements()
