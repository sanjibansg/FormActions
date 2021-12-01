from utils import logger
from db import model


def db_health():
    """Function for checking database health

    :return status: Dictionary with the current status of the database

    """
    logging = logger("db health")
    status = {"db_health": "unavailable"}
    try:
        db_model = model()
        logging.info("Health checking for CassandraDB")
        session = db_model.get_session_object()
        session.execute("SELECT now() from system.local;")
        status = {"db_health": "up and running"}
    except Exception:
        logging.exception("Health check for CassandraDB failed ", exc_info=True)
    return status
