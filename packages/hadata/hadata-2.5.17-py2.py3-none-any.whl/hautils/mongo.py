import os
from mongoengine import connect
from dotenv import load_dotenv

from hautils import logger

load_dotenv(override=False)

DATABASE_HOST = os.getenv('MONGO_HOST')
DATABASE_NAME = os.getenv('MONGO_DB')
DATABASE_USER = os.getenv("MONGO_USER")
DATABASE_PASS = os.getenv("MONGO_PASS")
DATABASE_PORT = os.getenv("MONGO_PORT", 27017)


def create_db():
    db_str = "mongodb://%s:%s@%s:%s/%s?authSource=admin" % (
        DATABASE_USER, DATABASE_PASS, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME)
    logger.logger.info("connecting to database string %s" % (db_str,))
    return connect(host=db_str)


def find_one_by_id(doc, oid):
    return doc.objects(id=oid).first()
