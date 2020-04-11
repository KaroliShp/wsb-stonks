from flask import jsonify
from app import app, db_client
from datetime import datetime, timedelta


@app.route('/api/', methods=['GET'])
def home():
    return "Hello World"


@app.route('/api/stock/frequency/top', methods=['GET'])
def stock_frequency_top():
    """
    Display current stock frequency from database (top)
    """
    stock_frequency = db_client.find_all('stock-frequency-top', {})
    return jsonify(stock_frequency[:10])


@app.route('/api/stock/frequency/historic/<string:stock_name>', methods=['GET'])
def stock_frequency_historic(stock_name):
    """
    Display current stock frequency from database (historic)
    """
    stock_frequency = db_client.find_all('stock-frequency-historic', { 'stock_name' : stock_name.upper() })[0]['historic_data']
    stock_frequency.reverse()
    return jsonify(stock_frequency)


@app.route('/api/stock/list', methods=['GET'])
def stock_list():
    """
    Display all stocks
    """
    stocks = db_client.find_all('stock-list', {})
    return jsonify(stocks)


@app.route('/api/keyword/top', methods=['GET'])
def keyword_top():
    """
    Display top keywords
    """
    top_keywords = db_client.find_all('keywords-top', {})
    top_keywords = sorted(list(filter(lambda x : " " in x['keyword'], top_keywords)), key=lambda x : x['mentions'], reverse=True)
    return jsonify(top_keywords[:10])


@app.route('/api/emoji/top', methods=['GET'])
def emoji_top():
    """
    Display top emojis
    """
    top_emoji = db_client.find_all('emoji-top', {})
    return jsonify(top_emoji[:10])


@app.route('/api/statistics', methods=['GET'])
def statistics():
    """
    Display statistics
    """
    statistics = db_client.find_all('statistics', {})[0]
    return jsonify(statistics)