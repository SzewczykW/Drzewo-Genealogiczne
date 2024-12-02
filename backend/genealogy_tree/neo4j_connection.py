from django.conf import settings
from neo4j import GraphDatabase

_driver = None


def get_session():
    global _driver
    if not _driver:
        _driver = GraphDatabase.driver(
            settings.NEO4J_URI, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
        )
    return _driver.session(database=settings.NEO4J_DB_NAME)
