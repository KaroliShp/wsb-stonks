import enum
from datetime import datetime, timedelta


# Top frequencies


def get_stock_freq_top(db_client):
    print(f'Start calculating stock frequency top')

    # Get raw frequency info from DB
    last_day = datetime.now() - timedelta(hours=24, minutes=0)
    raw_data_all = db_client.find_all('posts-data', { 'date' : { "$gt" : last_day } })
    
    # Find frequencies of all mentioned stocks
    top_frequency = {}
    for raw_data in raw_data_all:
        for data in raw_data['stocks']:
            if data['stock_name'] in top_frequency:
                top_frequency[data['stock_name']] += data['mentions']
            else:
                top_frequency[data['stock_name']] = data['mentions']

    print('Finish calculating stock frequency top')
    
    # Sort and return
    return [ { 'stock_name' : k, 'mentions' : v } for k, v in sorted(top_frequency.items(), key=lambda item: item[1], reverse=True)]


# Historic frequency calculations


def get_stock_freq_historic(db_client):
    print(f'Start calculating stock frequency history')

    # Get all info from DB
    posts_data = db_client.find_all('posts-data', {})

    # Get all mentioned stocks and all possible updates
    all_updates = []
    all_stocks = {}
    for raw_data in posts_data:
        all_updates.append(raw_data['date'])
        for data in raw_data['stocks']:
            if data['stock_name'] in all_stocks:
                all_stocks[data['stock_name']] += [ { 'time' : raw_data['date'], 'amount' : data['mentions'] } ]
            else:
                all_stocks[data['stock_name']] = [ { 'time' : raw_data['date'], 'amount' : data['mentions'] } ]

    # Fill mention gaps - insert 0 mentions for where the dates are not available
    for stock, value in all_stocks.items():
        # Updates where the stock was mentioned (%Y-%m-%d %H:%M format)
        updates = set([data['time'].strftime("%Y-%m-%d %H:%M") for data in value])
        for expected_update in all_updates:
            if expected_update.strftime("%Y-%m-%d %H:%M") not in updates:
                all_stocks[stock] += [ { 'time' : expected_update, 'amount' : 0  } ]

    # Restructure data
    stocks = []
    for key, val in all_stocks.items():
        # Sort and change date representation to just %H:%M for website
        historic_data = sorted(val, key=lambda x : x['time'], reverse=True)
        historic_data = list(map(lambda x : { 'amount' : x['amount'], 'time' : x['time'].strftime("%H:%M") }, historic_data))
        stocks.append({
            'stock_name' : key,
            'historic_data' : historic_data
        })

    print('Finish calculating stock frequency history')

    return stocks