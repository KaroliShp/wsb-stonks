from flask import Flask
from flask_cors import CORS
from config import Config
from app.mongo_client import MongoPostRepository
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import json 

from app.background_job.post_fetcher import fetch_posts, fetch_comments
from app.background_job.post_processor import process_posts
from app.background_job.stock_frequency import get_stock_freq_historic, get_stock_freq_top
from app.background_job.keyword_top import get_keywords_top
from app.background_job.emoji_top import get_emoji_top
from app.background_job.statistics_calculator import calculate_statistics
from app.background_job.stock_list import get_all_stocks
from nlp_engine.analysis import get_top_keywords_pytextrank
from app.background_job.global_state_update import update_top_stocks, update_top_emojis, update_total_stats

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

""" 
production = True
if production:
    sentry_sdk.init(
        dsn="https://c711d9c16fc043dd897d35d569c8a92d@o378312.ingest.sentry.io/5201503",
        integrations=[FlaskIntegration()]
    )
""" 

# Handle application creation
app = Flask(__name__)
app.config.from_object(Config)

# CORS
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Setup Logging
import logging

app.logger.setLevel(logging.DEBUG)
logger_ref = app.logger

# Handle database connection
db_client = MongoPostRepository('wsb-stonks-dev', logger_ref)


# Job scheduling
def background_job():
    # Get the latest update
    app.logger.debug("Started background job")
    start_date = datetime.utcnow().replace(microsecond=0)  # current update time
    end_date = start_date - timedelta(hours=1)
    limit_posts = 50
    limit_comments = 500

    # The following code will collect new hour stats

    # Fetch new created posts since last update
    #new_posts= fetch_posts(db_client, start_date, end_date, limit_posts)
    #new_comments = fetch_comments(db_client, start_date, end_date, limit_comments)
    new_posts = []
    with open('posts.txt') as f:
        new_posts = json.load(f)

    new_comments = []
    with open('comments.txt') as f:
        new_comments = json.load(f)

    # Calculate statistics
    db_statistics = calculate_statistics(db_client, new_posts, new_comments, start_date, end_date)
    new_entries = new_posts + new_comments
    db_top_stocks, db_top_emojis  = process_posts(db_client, new_entries, start_date, end_date)

    # Save all info into DB for this time slot
    app.logger.debug('Writing everything to DB')

    #db_client.delete_many('statistics', {})
    db_client.create('statistics', db_statistics)

    #db_client.delete_many('top-stocks', {})
    db_client.create('top-stocks', db_top_stocks)

    #db_client.delete_many('top-emojis', {})
    db_client.create('top-emojis', db_top_emojis)

    # Update total counts
    db_global_stocks_top = update_top_stocks(db_client)
    db_client.delete_many('top-stocks-global', {})
    db_client.create_many('top-stocks-global', db_global_stocks_top)

    db_global_emojis_top = update_top_emojis(db_client)
    db_client.delete_many('top-emojis-global', {})
    db_client.create_many('top-emojis-global', db_global_emojis_top)

    db_global_stats_top = update_total_stats(db_client, start_date)
    db_client.delete_many('top-stats-global', {})
    db_client.create('top-stats-global', db_global_stats_top)

    # Then increase/decrease overall stats by deleting last update
    # TODO

    app.logger.debug('Job completed')

"""
scheduler = BackgroundScheduler(timezone="US/Eastern")
scheduler.add_job(func=background_job, trigger="interval", minutes=12)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
"""

background_job()

# Other stuff
from app import routes