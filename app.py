from flask import Flask, jsonify
from flask_cors import CORS
from nsepython import *

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "NSE API is running"

# Get stock quote
@app.route('/stock/<symbol>')
def get_stock(symbol):
    try:
        data = nse_eq(symbol.upper())

        response = {
            "symbol": symbol.upper(),
            "price": data.get("priceInfo", {}).get("lastPrice"),
            "open": data.get("priceInfo", {}).get("open"),
            "high": data.get("priceInfo", {}).get("intraDayHighLow", {}).get("max"),
            "low": data.get("priceInfo", {}).get("intraDayHighLow", {}).get("min"),
            "volume": data.get("securityWiseDP", {}).get("quantityTraded"),
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Option Chain
@app.route('/option-chain/<symbol>')
def option_chain(symbol):
    try:
        data = nse_optionchain_scrapper(symbol.upper())
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)