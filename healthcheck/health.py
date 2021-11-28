from utils import logger

def db_health(session):
    logging=logger()
    status=True
    try:
        logging.info("Health checking for CassandraDB")
        session.execute('SELECT 1')
    except Exception:
        logging.exception("Health check for CassandraDB failed ",exc_info=True)
        status = False
    return status

def redis_health(queue):
    logging=logger()
    status=True
    try:
        logging.info("Health checking for Redis server")
        queue.ping()
    except Exception:
        logging.exception("Health check for Redis server failed ",exc_info=True)
        status=False
    return status
