import logging
import logging.handlers
import time
from app_config import config

# datetime | logger name | log level | filepath:line number | function | msg
LOG_FORMAT = '%(asctime)s | %(name)s | %(levelname)s | %(pathname)s:%(lineno)d | %(funcName)s | %(message)s'
formatter = logging.Formatter(LOG_FORMAT)
LOG_FILENAME = "gethome" + time.strftime('_%Y%m%d') + '.log'
rotate_file_handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME, maxBytes=1024*100, backupCount=5)
rotate_file_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(rotate_file_handler)
logger.setLevel(level=logging.DEBUG)


## setup google cloud logging
# import google.cloud.logging # Don't conflict with standard logging
# from google.cloud.logging.handlers import CloudLoggingHandler, setup_logging
# client = google.cloud.logging.Client()
# handler = CloudLoggingHandler(client)
# setup_logging(handler)

from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = config['env_vars']['SESSION_SECRET_KEY']

from flask_login import LoginManager
login_manager = LoginManager(app)

import GetHome.views