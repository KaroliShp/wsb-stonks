def process_posts(db_client, posts, update_date):
    """
    Process posts by extracting information from raw posts such as keywords, stock mentions and put into DB
    """
    print(f'Start processing posts')

    posts_processed = {}
    posts_processed['date'] = update_date

    # Feed new posts into NLP engine to perform frequency calculations
    stock_frequencies = { 'SPY' : 10, 'LOL' : 2 }
    posts_processed = { **posts_processed, **stock_frequencies }

    # Add information to DB
    db_client.create('posts-data', posts_processed)

    print('Done with processing posts')

    return stock_frequencies