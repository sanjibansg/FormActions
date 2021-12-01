from utils import logger

from redis import Redis
from rq import Queue


def redis_health():
    """Function for checking redis health

    :return status: Dictionary with the current status of redis server

    """
    logging = logger("redis health")
    status = {"redis_health": "unavailable"}
    try:
        redis_conn = Redis()
        logging.info("Health checking for Redis server")
        redis_conn.ping()
        status = {"redis_health": "up and running"}
    except Exception:
        logging.exception("Health check for Redis server failed ", exc_info=True)
    return status
