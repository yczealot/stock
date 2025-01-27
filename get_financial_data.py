import requests
import json

# Set your API key
API_KEY = "test"
BASE_URL = "https://open.lixinger.com/api"

# Define the endpoint
endpoint = f"{BASE_URL}/hk/company/fs/non_financial"

# Generate quarterly dates from 2021 to 2024
years = range(2021, 2025)
quarters = ["03-31", "06-30", "09-30", "12-31"]
dates = [f"{year}-{quarter}" for year in years for quarter in quarters]

print("Date, Net Profit (in billion), YoY Change (%), QoQ Change (%)")
for date in dates:
    payload = {
        "token": API_KEY,
        "date": date,
        "stockCodes": ["00883"],  # Stock code for CNOOC (China National Offshore Oil Corporation)
        # 主营业务收入：q.ps.oi.c_o 净利润：q.ps.oi.c_o
        "metricsList": ["q.ps.oi.c_o", "q.ps..c_y2y", "q.ps.npatshaoehopc.c_c2c"]  # Net profit, YoY, QoQ
    }

    try:
        # Send the request to the API
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()

        # Parse the response
        data = response.json()

        # Extract and format the data
        results = data.get("data", [])

        if not results:
            print(f"{date}, No data available.")
        else:
            for entry in results:
                net_profit = entry.get("q", {}).get("ps", {}).get("oi", {}).get("c_o", 0)
                yoy_change = entry.get("q", {}).get("ps", {}).get("oi", {}).get("c_y2y", None)
                qoq_change = entry.get("q", {}).get("ps", {}).get("oi", {}).get("c_c2c", None)

                # Convert net profit to billions and format to 1 decimal place
                net_profit_in_billion = net_profit / 1e8

                # Format YoY and QoQ changes as percentages with 1 decimal place
                yoy_change_percent = f"{yoy_change * 100:.1f}%" if yoy_change is not None else "N/A"
                qoq_change_percent = f"{qoq_change * 100:.1f}%" if qoq_change is not None else "N/A"

                print(f"{date}, {net_profit_in_billion:.1f}, {yoy_change_percent}, {qoq_change_percent}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred for date {date}: {e}")
    except KeyError as e:
        print(f"Unexpected data format for date {date}: {e}")
