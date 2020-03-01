from flask import Flask
from config import Config
from app.mongo_client import MongoPostRepository


# Handle application creation
app = Flask(__name__)
app.config.from_object(Config)

# Handle database connection
db_client = MongoPostRepository('wsb-stonks')

from app import routes