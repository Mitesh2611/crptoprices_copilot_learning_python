import requests
import csv
import datetime

crypto_data = []

def fetch_crypto_data():
    global crypto_data
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": "false"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        crypto_data = [
            {
                "symbol": coin["symbol"].upper(),
                "price": coin["current_price"]
            } for coin in data
        ]
        save_crypto_to_csv()
    except Exception as e:
        print(f"Error fetching crypto data: {e}")

def save_crypto_to_csv():
    with open('crypto_prices.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Symbol', 'Price', 'DateTime'])
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for coin in crypto_data:
            writer.writerow([coin['symbol'], coin['price'], current_time])

