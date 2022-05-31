import requests
import time
import os
from credentials import STOCK_API_KEY, NEWS_API_KEY

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## GET THE STOCK INFO
# connect to the API
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}
data = requests.get(url="https://www.alphavantage.co/query", params=stock_parameters)
stock_info = data.json()
# make it possible to fetch the closing values of the 2 previous trading days
values = stock_info["Time Series (Daily)"].values()
iter_object = iter(values)
# get the previous trading day close value
previous_trading_day = float(next(iter_object)["4. close"])
# get the closing value of the day before previous trading day
pre_previous_trading_day = float(next(iter_object)["4. close"])

print(type(previous_trading_day))
print(previous_trading_day)
print(type(pre_previous_trading_day))
print(pre_previous_trading_day)

# get the difference between 2 closes in %
difference = abs(previous_trading_day - pre_previous_trading_day)
print(difference)
percent_difference = round(difference * 100 / previous_trading_day, 1)
print(percent_difference)

# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def major_event():
    if percent_difference >= 5:
        return True
    else:
        return False

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
# if the change was negative, make the percent_difference negative
#
# #Optional: Format the SMS message like this:
# """
# TSLA: 🔺2%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# or
# "TSLA: 🔻5%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
