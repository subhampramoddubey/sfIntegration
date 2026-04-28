from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# NSE headers to avoid blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
}

# Create session (important)
session = requests.Session()


@app.route('/')
def home():
    return "NSE API is running"


# 🔥 Helper function to fetch NSE data safely
def get_nse_data(symbol):
    try:
        # Step 1: Hit NSE homepage (sets cookies)
        session.get("https://www.nseindia.com", headers=HEADERS, timeout=5)

        # Step 2: Fetch stock data
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        response = session.get(url, headers=HEADERS, timeout=5)

        return response.json()

    except Exception as e:
        return {"error": str(e)}


# ✅ Get stock quote
@app.route('/stock/<symbol>')
def get_stock(symbol):
    try:
        data = get_nse_data(symbol.upper())

        # Handle API failure
        if "error" in data:
            return jsonify(data), 500

        price_info = data.get("priceInfo", {})

        response = {
            "symbol": symbol.upper(),
            "price": price_info.get("lastPrice"),
            "open": price_info.get("open"),
            "high": price_info.get("intraDayHighLow", {}).get("max"),
            "low": price_info.get("intraDayHighLow", {}).get("min"),
            "volume": data.get("marketDeptOrderBook", {}).get("tradeInfo", {}).get("totalTradedVolume"),
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Option Chain (still using nsepython fallback OR can upgrade later)
@app.route('/option-chain/<symbol>')
def option_chain(symbol):
    try:
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol.upper()}"

        session.get("https://www.nseindia.com", headers=HEADERS, timeout=5)
        response = session.get(url, headers=HEADERS, timeout=5)

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)