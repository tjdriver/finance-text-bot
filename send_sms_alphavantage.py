# below code is copied from twilio documentation

import os
from twilio.rest import Client
import requests

av_apikey = os.environ['AV_APIKEY']
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
from_number = os.environ['TWILIO_FROM_NUM']
to_number = os.environ['TWILIO_TO_NUM']
dad_number = os.environ['TWILIO_DAD_NUM']

params = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': 'okta',
    'apikey': av_apikey,
}

response = requests.get('http://www.alphavantage.co/query', params)
api_response = response.json()
# print(api_response)

# convert into list
prev_closes = list(api_response['Time Series (Daily)'].values())

# get the data for the last 5 days
closing_price = float(prev_closes[0]["4. close"])
# print('this is the closing price', closing_price)

# get the average of the last five days' closing
total = 0
for x in range(5):
    total += float(prev_closes[x]['4. close'])

moving_avg = total / 5

# get the day change
day_change = (float(prev_closes[0]['4. close']) - \
              float(prev_closes[1]['4. close'])) / float(prev_closes[1]['4. close']) * 100

first_line = 'Date: %s\n'%list(api_response['Time Series (Daily)'])[0]
second_line = 'Price of Okta: %.2f\n'%closing_price
third_line = 'Change: %.2f%%\n'%day_change
fourth_line = '5 Day Moving Avg: %.2f\n'%moving_avg


# get RIVN Data

params2 = params
params2['symbol'] = 'rivn'

response2 = requests.get('http://www.alphavantage.co/query', params2)
rivn_response = response2.json()
fifth_line = 'Price of RIVN: %.2f\n'%float(list(rivn_response['Time Series (Daily)'].values())[0]['4. close'])


# get SOL data

params3 = {
    'function': 'CURRENCY_EXCHANGE_RATE',
    'from_currency': 'sol',
    'to_currency':'usd',
    'apikey': av_apikey
}

response3 = requests.get('http://www.alphavantage.co/query', params3)
sol_response = response3.json()
sixth_line = 'Price of SOL: %.2f'%float( \
    sol_response['Realtime Currency Exchange Rate']['5. Exchange Rate'])


# print(first_line, second_line, third_line, fourth_line, '\n', fifth_line, sixth_line)

#  get the sid and auth tokens from twilio console
client = Client(account_sid, auth_token)

message = client.messages.create(
       body = first_line + second_line + third_line + fourth_line + '\n' +  fifth_line + sixth_line,
       from_= from_number,
       to= to_number
   )


message = client.messages.create(
       body = first_line + second_line + third_line + fourth_line + '\n' +  fifth_line + sixth_line,
       from_= from_number,
       to= dad_number
   )
 # print(message.sid)




