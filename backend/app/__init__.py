from flask import Flask
from config import Config
from app.mongo_client import MongoPostRepository

import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

from app.tasks.tasks import update_posts, get_posts, update_companies, get_companies, update_frequency_statistics
from app.tasks.nlp_engine.analysis import tokenize_posts, tokenize_posts_mwe, lemmatize_words, get_stock_frequency
from app.background_job.post_fetcher import fetch_posts
from app.background_job.stock_frequency import calculate_stock_frequency

# Handle application creation
app = Flask(__name__)
app.config.from_object(Config)

# Handle database connection
db_client = MongoPostRepository('wsb-stonks')

def job_update_db():
    print('Starting a job')
    update_companies(db_client)
    update_posts(db_client)
    symbols, company_names = get_companies(db_client)
    update_frequency_statistics(db_client, get_posts(db_client), symbols, company_names)
    print('Job finished')

def background_job():
    # Get the latest update
    last_update = datetime.now() - timedelta(hours=1, minutes=0)
    
    # Fetch new created posts since last update
    new_posts = fetch_posts(db_client, last_update)

    # Calculate stock frequency of the new posts
    calculate_stock_frequency(new_posts)

    # Update frequency tables


# Job scheduling
"""
scheduler = BackgroundScheduler(timezone="US/Eastern")
scheduler.add_job(func=job_update_db, trigger="interval", minutes=1)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
"""

#job_update_db()
background_job()

from app import routes