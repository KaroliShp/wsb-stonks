from flask import Flask
from config import Config
from app.mongo_client import MongoPostRepository

import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from app.tasks.tasks import update_posts, get_posts, update_companies, get_companies, update_frequency_statistics
from app.tasks.nlp_engine.analysis import tokenize_posts, tokenize_posts_mwe, lemmatize_words, get_stock_frequency
from app.background_job.post_fetcher import fetch_posts

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
    fetch_posts(db_client)

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