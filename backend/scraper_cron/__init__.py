from flask import Flask
from config import Config
from app.mongo_client import MongoPostRepository

from datetime import datetime, timedelta

from scraper_cron.background_job.post_fetcher import fetch_posts
from scraper_cron.background_job.post_processor import process_posts
from scraper_cron.background_job.stock_frequency import get_stock_freq_historic, get_stock_freq_top
from scraper_cron.background_job.keyword_top import get_keywords_top
from scraper_cron.background_job.emoji_top import get_emoji_top
from scraper_cron.background_job.statistics_calculator import calculate_statistics
from scraper_cron.background_job.stock_list import get_all_stocks

from nlp_engine.analysis import get_top_keywords_pytextrank

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

production = True
if production:
    sentry_sdk.init(
        dsn="https://c711d9c16fc043dd897d35d569c8a92d@o378312.ingest.sentry.io/5201503",
        integrations=[FlaskIntegration()]
    )

# Handle application creation
app = Flask(__name__)
app.config.from_object(Config)

# Setup Logging
import logging

app.logger.setLevel(logging.DEBUG)
logger_ref = app.logger

# Handle database connection
db_client = MongoPostRepository('wsb-stonks', logger_ref)

# Setup cron job endpoint
@app.route('/scraper')
def background_job():
    try:
        # Get the latest update
        app.logger.debug("Started background job")
        update_date = datetime.utcnow().replace(microsecond=0)  # current update time
        num_of_updates = 24  # how many hours to update (assume we update once an hour)
        limit = 150  # upper limit of how many posts appeared since last update

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
        #db_top_keywords_list = get_keywords_top(db_client)
        db_top_keywords_list = get_top_keywords_pytextrank(new_entries_by_date)

        # Get top emoji
        db_top_emoji_list = get_emoji_top(db_client)

        # Write everything to DB at once
        app.logger.debug('Writing everything to DB')
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

        # Get all mentioned stocks
        db_all_stocks = get_all_stocks(db_client)

        db_client.delete_many('stock-list', {})
        db_client.create_many('stock-list', db_all_stocks)
        app.logger.debug('Job completed')
        
        return "Success", 200 
    
    except Exception as e:
        app.logger.warning("Critical error")
        app.logger.warning(e.with_traceback)
        return "Failed", 404