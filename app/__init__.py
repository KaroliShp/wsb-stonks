from flask import Flask, jsonify
from app.db.mongo_client import MongoPostRepository

app = Flask(__name__)

db_client = MongoPostRepository('wsb-stonks')


@app.route('/stock/frequency')
def stock_frequency():
    """
    Display current stock frequency from database
    """
    stock_frequency = db_client.find_all('analysis-stock-frequency', {})
    return jsonify(stock_frequency)
    