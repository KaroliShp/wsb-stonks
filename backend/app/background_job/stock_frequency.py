import enum
from datetime import datetime, timedelta


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

    # Get all info from DB
    info_all = db_client.find_all('posts-data', {})

    # Get all updates
    all_updates = []
    for info in info_all:
        all_updates.append(info['date'].strftime("%H:%M"))

    print(all_updates)

    # Get all mentioned stocks
    all_stocks = {}
    for info in info_all:
        for key, val in info.items():
            if key not in NON_STOCK_FIELDS and str(key).lower() in all_stocks:
                all_stocks[str(key).lower()] += [ { 'time' : info['date'].strftime("%H:%M"), 'amount' : val } ]
            elif key not in NON_STOCK_FIELDS:
                all_stocks[str(key).lower()] = [ { 'time' : info['date'].strftime("%H:%M"), 'amount' : val } ]

    # Insert 0 for where dates are not available
    for stock, value in all_stocks.items():
        updates = set([data['time'] for data in value])
        for expected_update in all_updates:
            if expected_update not in updates:
                all_stocks[stock] += [ { 'time' : expected_update, 'amount' : 0  } ]

    # Restructure data
    stocks = []
    for key, val in all_stocks.items():
        stocks.append({
            'stock_name' : key,
            'historic_data' : val
        })

    db_client.delete_many('stock-frequency-historic', {})
    db_client.create_many('stock-frequency-historic', stocks)

    print('Finish calculating stock frequency history')


"""
def get_stock_freq_historic(db_client, stock_frequency, update_date):
    print(f'Start updating stock frequency history')

    for stock, mentions in stock_frequency:
        db_client.update('stock-frequency-historic', { 'stock_name' : str(stock) }, { '$push' : { 'historic_frequency' : { 'date' : update_date, 'mentions' : mentions } } })

    print('Finish updating stock frequency history')
"""