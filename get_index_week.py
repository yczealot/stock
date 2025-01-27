import requests
import datetime
import pandas as pd

# Define the API URL and parameters
api_url = "https://open.lixinger.com/api/hk/index/candlestick"

# Token and stock code for CSI 300 Index (assuming the token is obtained)
api_token = "test"
stock_code = "HSTECH"  # Assuming this is the CSI 300 code from the example

def get_fridays(start_date, end_date):
    current_date = start_date
    fridays = []
    while current_date <= end_date:
        if current_date.weekday() == 4:  # Friday is represented by 4
            fridays.append(current_date)
        current_date += datetime.timedelta(days=1)
    return fridays

# Get the dates
start_date = datetime.datetime.strptime("2024-05-17", "%Y-%m-%d")
end_date = datetime.datetime.now()
fridays = get_fridays(start_date, end_date)

# Iterate over Fridays and collect closing prices
data = []
for friday in fridays:
    params = {
        "token": api_token,
        "type": "normal",
        "startDate": friday.strftime("%Y-%m-%d"),
        "endDate": friday.strftime("%Y-%m-%d"),
        "stockCode": stock_code
    }

    response = requests.post(api_url, json=params)

    if response.status_code == 200:
        response_data = response.json()
        if "data" in response_data and len(response_data["data"]) > 0:
            closing_price = response_data["data"][0]["close"]
            data.append([friday.strftime('%Y-%m-%d'), closing_price])
        else:
            data.append([friday.strftime('%Y-%m-%d'), None])
    else:
        data.append([friday.strftime('%Y-%m-%d'), None])

# Create a DataFrame and display the table
df = pd.DataFrame(data, columns=["Date", "Closing Price"])
print(df)
