from flask import jsonify
from flask_cors import cross_origin
from app import app, db_client
from datetime import datetime, timedelta


@app.route('/api/', methods=['GET'])
@cross_origin()
def home():
    return "Hello World"


@app.route('/api/stock/frequency/top', methods=['GET'])
@cross_origin()
def stock_frequency_top():
    """
    Display current stock frequency from database (top)
    """
    stock_frequency = db_client.find_all('stock-frequency-top', {})
    return jsonify(stock_frequency[:10])


@app.route('/api/stock/frequency/historic/<string:stock_name>', methods=['GET'])
@cross_origin()
def stock_frequency_historic(stock_name):
    """
    Display current stock frequency from database (historic)
    """
    stock_frequency = db_client.find_all('stock-frequency-historic', { 'stock_name' : stock_name.upper() })[0]['historic_data']
    stock_frequency.reverse()
    return jsonify(stock_frequency)


@app.route('/api/stock/list', methods=['GET'])
@cross_origin()
def stock_list():
    """
    Display all stocks
    """
    stocks = db_client.find_all('stock-list', {})
    return jsonify(stocks)


@app.route('/api/keyword/top', methods=['GET'])
@cross_origin()
def keyword_top():
    """
    Display top keywords
    """
    top_keywords = db_client.find_all('keywords-top', {})
    return jsonify(top_keywords[:10])


@app.route('/api/emoji/top', methods=['GET'])
@cross_origin()
def emoji_top():
    """
    Display top emojis
    """
    top_emoji = db_client.find_all('emoji-top', {})
    return jsonify(top_emoji[:10])


@app.route('/api/statistics', methods=['GET'])
@cross_origin()
def statistics():
    """
    Display statistics
    """
    statistics = db_client.find_all('statistics', {})[0]
    return jsonify(statistics)


@app.route('/api/statistics/activity/posts', methods=['GET'])
@cross_origin()
def statistics_activity_posts():
    """
    Display post activity statistics
    """
    statistics = db_client.find_all('statistics', {})[0]['posts_activity']
    statistics.reverse()
    return jsonify(statistics)


@app.route('/api/statistics/activity/comments', methods=['GET'])
@cross_origin()
def statistics_activity_comments():
    """
    Display comment activity statistics
    """
    statistics = db_client.find_all('statistics', {})[0]['comments_activity']
    statistics.reverse()
    return jsonify(statistics)