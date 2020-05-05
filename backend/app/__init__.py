from flask import Flask
from flask_cors import CORS
from config import Config
from app.mongo_client import MongoPostRepository

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

# CORS
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Setup Logging
import logging

app.logger.setLevel(logging.DEBUG)
logger_ref = app.logger

# Handle database connection
db_client = MongoPostRepository('wsb-stonks', logger_ref)

# Other stuff
from app import routes