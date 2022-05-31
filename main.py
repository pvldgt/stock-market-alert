import requests

from credentials import STOCK_API_KEY, NEWS_API_KEY

STOCK = "AMZN"
COMPANY_NAME = "Amazon"

## GET THE STOCK INFO
# connect to the API
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}
data = requests.get(url="https://www.alphavantage.co/query", params=stock_parameters)
stock_info = data.json()
print(stock_info)
# make it possible to fetch the closing values of the 2 previous trading days
values = stock_info["Time Series (Daily)"].values()
iter_object = iter(values)
# get the previous trading day close value
previous_trading_day = float(next(iter_object)["4. close"])
# get the closing value of the day before previous trading day
pre_previous_trading_day = float(next(iter_object)["4. close"])

# print(type(previous_trading_day))
# print(previous_trading_day)
# print(type(pre_previous_trading_day))
# print(pre_previous_trading_day)

# get the difference between 2 closes in %
difference = abs(previous_trading_day - pre_previous_trading_day)
# print(difference)
percent_difference = round(difference * 100 / previous_trading_day, 1)
# print(percent_difference)

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
# api setup
news_parameters = {
    "q": COMPANY_NAME,
    "category": "business",
    "language": "en",
    "country": "us",
    "apiKey": NEWS_API_KEY
}
data = requests.get(url="https://newsapi.org/v2/top-headlines", params=news_parameters)
news = data.json()
print(news)

# create dictionary of top 3 stories
# top_stories_dict = {}
# for i in range(0, len(news["articles"])):
#     top_stories_dict[news["articles"][i]["title"]] = news["articles"][i]["description"]

# if there was a major event, send a test with 3 news pieces
if major_event():
    if previous_trading_day - pre_previous_trading_day < 0:
        percent_difference += -1
        emoji = "🔻"
    else:
        emoji = "🟢"
    if news["totalResults"] == 0:
        print(f"{STOCK}: {emoji} {percent_difference}")
    else:
        for news_item in range (0,3):
            print(f""""{STOCK}: {emoji} {percent_difference}
            {news["articles"][news_item]["title"]}
            {news["articles"][news_item]["description"]}""")

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
