from flask import Flask
from flask_cors import CORS
from config import Config
from app.mongo_client import MongoPostRepository
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

from app.background_job.post_fetcher import fetch_posts
from app.background_job.post_processor import process_posts
from app.background_job.stock_frequency import get_stock_freq_historic, get_stock_freq_top
from app.background_job.keyword_top import get_keywords_top
from app.background_job.emoji_top import get_emoji_top
from app.background_job.statistics_calculator import calculate_statistics
from app.background_job.stock_list import get_all_stocks


# Handle application creation
app = Flask(__name__)
app.config.from_object(Config)

# CORS
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Handle database connection
db_client = MongoPostRepository('wsb-stonks')

# Job scheduling
def background_job():
    # Get the latest update
    update_date = datetime.utcnow().replace(microsecond=0)  # current update time
    num_of_updates = 23  # how many hours to update (assume we update once an hour)
    limit = 400  # upper limit of how many posts appeared since last update
    
    # Fetch new created posts since last update
    new_entries_by_date = fetch_posts(db_client, update_date, num_of_updates, limit)

    # Calculate statistics
    db_statistics = calculate_statistics(db_client, new_entries_by_date, update_date)

    # Process post information
    db_posts_processed_all = []
    for date, new_entries in new_entries_by_date.items():
        db_posts_processed_all.append(process_posts(db_client, new_entries, date))
    db_client.delete_many('posts-data', {})
    for db_posts_processed in db_posts_processed_all:
        db_client.create('posts-data', db_posts_processed)

    # Calculate most frequent stocks from all posts historically
    db_top_frequency_list = get_stock_freq_top(db_client)

    # Calculate stock frequency of all posts historically
    db_stocks = get_stock_freq_historic(db_client)

    # Get the new keyword top
    db_top_keywords_list = get_keywords_top(db_client)

    # Get top emoji
    db_top_emoji_list = get_emoji_top(db_client)

    # Get all mentioned stocks
    db_all_stocks = get_all_stocks(db_client)

    # Write everything to DB at once
    print('Writing everything to DB')
    db_client.delete_many('statistics', {})
    db_client.create('statistics', db_statistics)

    db_client.delete_many('stock-frequency-top', {})
    db_client.create_many('stock-frequency-top', db_top_frequency_list)
    
    db_client.delete_many('stock-frequency-historic', {})
    db_client.create_many('stock-frequency-historic', db_stocks)

    db_client.delete_many('keywords-top', {})
    db_client.create_many('keywords-top', db_top_keywords_list)

    db_client.delete_many('emoji-top', {})
    db_client.create_many('emoji-top', db_top_emoji_list)

    db_client.delete_many('stock-list', {})
    db_client.create_many('stock-list', db_all_stocks)


"""
scheduler = BackgroundScheduler(timezone="US/Eastern")
scheduler.add_job(func=background_job, trigger="interval", minutes=15)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
"""

#background_job()

# Other stuff
from app import routes