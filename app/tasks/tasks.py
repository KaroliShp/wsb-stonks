from app.tasks.tasks_db import write_posts, retrieve_posts, write_companies, retrieve_companies, write_frequency
from app.tasks.nlp_engine.scraper import main
from app.tasks.nlp_engine.analysis import get_stock_frequency
from app.tasks.nlp_engine.io import read_stocks, read_from_file
from app.tasks.nlp_engine.analysis import get_stock_frequency

def update_posts(db_client):
    data = main()
    write_posts(db_client, data)


def get_posts(db_client):
    return retrieve_posts(db_client)


def update_companies(db_client):
    data = read_stocks()
    write_companies(db_client, data)


def get_companies(db_client):
    return retrieve_companies(db_client)


def update_frequency_statistics(db_client, posts, symbol_data):
    print(posts)
    print(symbol_data)
    data = get_stock_frequency(posts, symbol_data[0])
    print(data)
    write_frequency(db_client, data)