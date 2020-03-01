from flask import Flask
from config import Config
from app.mongo_client import MongoPostRepository

import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from app.tasks.tasks import update_posts, get_posts, update_companies, get_companies, update_frequency_statistics

# Handle application creation
app = Flask(__name__)
app.config.from_object(Config)

# Handle database connection
db_client = MongoPostRepository('wsb-stonks')

def job_update_db():
    print('Starting a job')
    update_companies(db_client)
    update_posts(db_client)
    update_frequency_statistics(db_client, get_posts(db_client), get_companies(db_client))
    print('Job finished')

# Job scheduling
"""
scheduler = BackgroundScheduler()
scheduler.add_job(func=job_update_db, trigger="interval", seconds=120)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
"""

from app import routes