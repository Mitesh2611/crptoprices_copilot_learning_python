from flask import Blueprint, jsonify, render_template
import threading
import time
from .crypto import fetch_crypto_data, crypto_data

main = Blueprint('main', __name__)

# Background thread to refresh data
def refresh_data_periodically():
    while True:
        fetch_crypto_data()
        time.sleep(300)

threading.Thread(target=refresh_data_periodically, daemon=True).start()
fetch_crypto_data()

@main.route('/')
def index():
    return render_template('index.html', crypto_data=crypto_data)

@main.route('/top-10-crypto', methods=['GET'])
def top_10_crypto_api():
    return jsonify(crypto_data[:10])

