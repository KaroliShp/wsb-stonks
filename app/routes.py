from flask import jsonify
from app import app, db_client

@app.route('/', methods=['GET'])
def home():
    return "Hello World"

@app.route('/stock/frequency', methods=['GET'])
def stock_frequency():
    """
    Display current stock frequency from database
    """
    stock_frequency = db_client.find_all('analysis-stock-frequency', {})
    return jsonify(stock_frequency[:10])