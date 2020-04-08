import enum
from datetime import datetime, timedelta


def calculate_stock_frequency(db_client, last_update = datetime.now() - timedelta(hours=0, minutes=30)):
    """
    Calculate stock mentions given posts and store in DB
    """
    print(f'Start calculating stock frequency')

    # Get raw posts from DB
    raw_posts = db_client.find_all('posts', {})

    # Filter new posts based on the creation date
    posts = list(filter(lambda x : datetime.utcfromtimestamp(x['created']) > last_update, raw_posts))
    print(len(posts))

    # Feed new posts into NLP engine to perform frequency calculations
    stock_frequency = { 'SPY' : 10, 'LOL' : 2 }

    # Add information to DB
    db_client.create('stock-frequency', {
        'date' : datetime.now(), 
        'frequency' : stock_frequency 
    })

    print('Done calculating stock frequency')
