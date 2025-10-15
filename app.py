from flask import Flask, render_template, send_file
import requests
import csv
import io

app = Flask(__name__)

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

@app.route('/')
def index():
    data = fetch_crypto_data()
    return render_template('index.html', data=data)

@app.route('/download')
def download_csv():
    data = fetch_crypto_data()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Name', 'Symbol', 'Current Price', 'Market Cap'])
    for coin in data:
        writer.writerow([coin['name'], coin['symbol'], coin['current_price'], coin['market_cap']])
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='crypto_prices.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)