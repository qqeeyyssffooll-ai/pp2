import psycopg2
from config import load_config


def connect():
    params = load_config()
    conn = psycopg2.connect(**params)
    return conn