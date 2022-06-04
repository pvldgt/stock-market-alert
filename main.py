import requests
from twilio.rest import Client
from credentials import STOCK_API_KEY, NEWS_API_KEY, \
    twilio_account_sid, twilio_auth_token, my_number, twilio_number

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

# get the stock info by connecting to the API
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

# get the difference between 2 closes in %
difference = abs(previous_trading_day - pre_previous_trading_day)
# print(difference)
percent_difference = round(difference * 100 / previous_trading_day, 1)


# When the stock price increases/decreases by 5% between yesterday and the day before yesterday then return True
def major_event():
    if percent_difference >= 5:
        return True
    else:
        return False


# if there was a major event, send an SMS alert with 3 news pieces
if major_event():
    # grab the 3 top news stories about the stock with the help of newsapi.org
    news_parameters = {
        "q": COMPANY_NAME,
        "language": "en",
        "apiKey": NEWS_API_KEY
    }
    data = requests.get(url="https://newsapi.org/v2/everything", params=news_parameters)
    news = data.json()

    if previous_trading_day - pre_previous_trading_day < 0:
        percent_difference += -1
        emoji = "🔻"
    else:
        emoji = "🟢"

    # set up the Twilio client
    client = Client(twilio_account_sid, twilio_auth_token)
    # if there is no news for the company, then just send the ticker and the percentage point
    if news["totalResults"] == 0:
        message = client.messages.create(
            body=f"{STOCK}: {emoji} {percent_difference}%",
            from_=twilio_number,
            to=my_number
        )
        print(message.status)
    # otherwise send the 3 news articles too
    else:
        try:
            for news_item in range(0, 3):
                message = client.messages.create(
                    body=f"""{STOCK}: {emoji} {percent_difference}%
                    \nTitle: {news["articles"][news_item]["title"]}
                    \nBrief: {news["articles"][news_item]["description"]}""",
                    from_=twilio_number,
                    to=my_number
                )
                print(message.status)
        except IndexError:
            print("There were fewer than 3 articles")
# don't send anything if there was no major event
else:
    print("There was no major event.")
