from flask import Flask
from config import Config
from app.mongo_client import MongoPostRepository
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

from app.background_job.post_fetcher import fetch_posts
from app.background_job.post_processor import process_posts
from app.background_job.stock_frequency import get_stock_freq_historic, get_stock_freq_top


# Handle application creation
app = Flask(__name__)
app.config.from_object(Config)

# Handle database connection
db_client = MongoPostRepository('wsb-stonks')

# Job scheduling
def background_job():
    # Get the latest update
    last_update = datetime.now() - timedelta(hours=1, minutes=0)
    update_date = datetime.now()
    
    # Fetch new created posts since last update
    new_posts = fetch_posts(db_client, last_update)

    # Process post information and store in DB
    process_posts(db_client, new_posts, update_date)

    # Calculate most frequent stocks from all posts historically
    get_stock_freq_top(db_client)

    # Calculate stock frequency of all posts historically
    # get_stock_freq_historic(db_client)

"""
scheduler = BackgroundScheduler(timezone="US/Eastern")
scheduler.add_job(func=background_job, trigger="interval", minutes=15)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
"""

background_job()

# Other stuff
from app import routes