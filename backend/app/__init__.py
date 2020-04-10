from flask import Flask
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

# Handle application creation
app = Flask(__name__)
app.config.from_object(Config)

# Handle database connection
db_client = MongoPostRepository('wsb-stonks')

# Job scheduling
def background_job():
    # Get the latest update
    update_date = datetime.now().replace(microsecond=0)  # current update time
    num_of_updates = 23  # how many hours to update (assume we update once an hour)
    limit = 100  # upper limit of how many posts appeared since last update
    
    # Fetch new created posts since last update
    new_posts_by_date = fetch_posts(db_client, update_date, num_of_updates, limit)

    # Calculate statistics
    calculate_statistics(db_client, new_posts_by_date, update_date)

    return None

    # Process post information and store in DB
    db_client.delete_many('posts-data', {})
    for date, new_posts in new_posts_by_date.items():
        process_posts(db_client, new_posts, date)

    # Calculate most frequent stocks from all posts historically
    get_stock_freq_top(db_client)

    # Calculate stock frequency of all posts historically
    get_stock_freq_historic(db_client)

    # Get the new keyword top
    get_keywords_top(db_client)

    # Get top emoji
    get_emoji_top(db_client)


"""
scheduler = BackgroundScheduler(timezone="US/Eastern")
scheduler.add_job(func=background_job, trigger="interval", minutes=15)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
"""

#background_job()

# Other stuff
from app import routes