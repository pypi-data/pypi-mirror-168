import logging
import os
import pathlib as pl
import time
from logging.handlers import RotatingFileHandler

import requests

# Constants
TEN_MEGABYTES = 10 * 1024 * 1024

# Omni directory - where this class lives.
Omnidir = pl.Path(__file__).parents[1]

# logs directory
logpath = Omnidir / "logs"
if os.path.exists(logpath):
    pass
else:
    os.makedirs(logpath)

# logging config
log_file_handler = RotatingFileHandler(
    logpath / "omniquestor.log", maxBytes=TEN_MEGABYTES, backupCount=10
)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s: %(message)s -- %(filename)s::%(funcName)s" " > line: %(lineno)d",
    "%b %d %H:%M:%S",
)
formatter.converter = time.gmtime
log_file_handler.setFormatter(formatter)
logger = logging.getLogger("omniquestor logger")
logger.addHandler(log_file_handler)


class Omniquestor:
    def __init__(self, url, headers, request_type, json=""):
        self.url = url
        self.headers = headers
        self.request_type = request_type
        self.json = json
        logger.info(
            "Omniquestor initialized with these values: "
            "\n\tURL: %s \n\tHeader: %s \n\tRequest Type: %s \n\tJSON: %s",
            self.url,
            self.headers,
            self.request_type,
            self.json,
        )

    def response(self):
        default = "Invalid"
        return getattr(self, str(self.request_type), lambda: default)()

    def get(self):
        logger.info("Performing a GET request")
        get_response = requests.get(self.url, headers=self.headers)
        logger.info("The GET response status code: %s", get_response.status_code)
        logger.info("The GET response details: %s", get_response.json())
        return get_response

    def post(self):
        logger.info("Performing a POST request")
        post_response = requests.post(self.url, headers=self.headers, json=self.json)
        logger.info("The POST response status code: %s", post_response.status_code)
        logger.info("The POST response details: %s", post_response.json())
        return post_response

    def put(self):
        logger.info("Performing a PUT request")
        put_response = requests.put(self.url, headers=self.headers, json=self.json)
        logger.info("The PUT response status code: %s", put_response.status_code)
        logger.info("The PUT response details: %s", put_response.json())
        return put_response

    def delete(self):
        logger.info("Performing a DELETE request")
        delete_response = requests.delete(self.url, headers=self.headers)
        logger.info("The DELETE response status code: %s", delete_response.status_code)
        logger.info("The DELETE response details: %s", delete_response.json())
        return delete_response
