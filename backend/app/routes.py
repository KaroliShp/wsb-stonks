from flask import jsonify
from app import app, db_client


@app.route('/api/', methods=['GET'])
def home():
    return "Hello World"


@app.route('/api/stock/frequency/top', methods=['GET'])
def stock_frequency():
    """
    Display current stock frequency from database
    """
    stock_frequency = db_client.find_all('stock-frequency-top', {})
    print(stock_frequency)
    return jsonify(stock_frequency[:10])


@app.route('/api/keyword/top', methods=['GET'])
def keyword_top():
    """
    Display top keywords
    """
    top_keywords = db_client.find_all('keywords-top', {})
    return jsonify(top_keywords[:10])