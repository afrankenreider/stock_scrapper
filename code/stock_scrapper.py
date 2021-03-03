from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time
from datetime import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

# create dataframe with the stocks we want to scrape
stock_symbols = [['PLUG'], ['APPS'], ['CHRW'], ['TSLA'], ['AAPL']]

s_df = pd.DataFrame(stock_symbols, columns=['stock_symbol'])
# putting my data in a list to loop over
l_list = s_df.values.tolist()

# define driver 
driver = webdriver.Chrome('/Users/afrankenreider/Downloads/chromedriver')

def call_web():
    driver.get('https://www.google.com/finance')

call_web()

# start loop here
for l in l_list:
    symbol = l[0]
    symbol_str = str(symbol)

    def find_stock_price():
        # find the search form, clear, and click... search symbol
        search_form = driver.find_element_by_xpath('//*[@id="search-bar"]')
        search_form.click()
        search_form.clear()
        search_form.send_keys(symbol)
        time.sleep(.5)

        # press ENTER
        search_form.send_keys(Keys.ENTER)

        # find current stock price
        stock_price = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[3]/main/div[2]/c-wiz/div/div[1]/div[1]/div/div[1]/div[1]/div/div[1]/div/span/div/div')))
        print("Current stock price for $"+symbol+" at "+current_time+" is -> ",stock_price.text)
        s_str = str(stock_price.text)

        # send email notification w/ current stock price
        sender_email = 'email address here'
        receiver_email = 'email address here'
        password = 'password here'

        message = MIMEMultipart("alternative")
        message["Subject"] = "$"+symbol_str+" price update: "+s_str
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = """\
        Watchlist price notification"""
        
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")

        # Add HTML/plain-text parts to MIMEMultipart message
        message.attach(part1)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

        call_web()

    find_stock_price()

driver.quit()
