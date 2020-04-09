import enum
from datetime import datetime, timedelta

from nlp_engine.analysis import get_stocks


NON_STOCK_FIELDS = ['date', '_id', 'top_keywords']


# Top frequencies


def get_stock_freq_top(db_client):
    print(f'Start calculating stock frequency top')

    # Get raw frequency info from DB
    last_day = datetime.now() - timedelta(hours=24, minutes=0)
    raw_data = db_client.find_all('posts-data', { 'date' : { "$gt" : last_day } })
    
    # Find frequencies of all mentioned stocks
    top_frequency = {}
    for data in raw_data:
        for key, value in data.items():
            if key not in NON_STOCK_FIELDS and key in top_frequency:
                top_frequency[key] += value
            elif key not in NON_STOCK_FIELDS:
                top_frequency[key] = value

    # Convert dictionary to list of tuples
    top_frequency_list = sorted([ { 'stock_name' : k, 'mentions' : v } for k, v in top_frequency.items() ], key=lambda x : x['mentions'], reverse=True)

    # Insert the information into DB
    db_client.delete_many('stock-frequency-top', {})
    db_client.create_many('stock-frequency-top', top_frequency_list)

    print('Finish calculating stock frequency top')


# Historic frequency calculations


def get_stock_freq_historic(db_client):
    print(f'Start calculating stock frequency history')

    # Get all stocks
    stocks = get_stocks()

    for stock, _ in stocks:
        # Get raw frequency info from DB
        raw_data = db_client.find_all('posts-data', { str(stock) : { "$exists" : True } })
        
        # If such stock has been mentioned
        if len(raw_data) > 0:
            historic_frequency = [ { 'date' : post['date'], 'mentions' : post[str(stock)] } for post in raw_data ]

            # Update stock historic information on DB
            db_client.create('stock-frequency-historic', {
                'stock_name' : str(stock),
                'historic_frequency' : historic_frequency
            })

    print('Finish calculating stock frequency history')


"""
def get_stock_freq_historic(db_client, stock_frequency, update_date):
    print(f'Start updating stock frequency history')

    for stock, mentions in stock_frequency:
        db_client.update('stock-frequency-historic', { 'stock_name' : str(stock) }, { '$push' : { 'historic_frequency' : { 'date' : update_date, 'mentions' : mentions } } })

    print('Finish updating stock frequency history')
"""