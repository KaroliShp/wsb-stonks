from nlp_engine.analysis import get_stock_frequency, get_top_keywords


def process_posts(db_client, posts, update_date):
    """
    Process posts by extracting information from raw posts such as keywords, stock mentions and put into DB
    """
    print(f'Start processing posts')

    posts_processed = {}
    posts_processed['date'] = update_date

    # Feed new posts into NLP engine to perform frequency calculations
    stock_frequencies = get_stock_frequency(posts)
    posts_processed = { **posts_processed, **stock_frequencies }

    # Feed new posts into NLP engine to perform keyword analysis
    top_keywords = { 'top_keywords' : get_top_keywords(posts) }
    posts_processed = {**posts_processed, **top_keywords}

    # Add information to DB
    db_client.delete_many('posts-data', {})
    db_client.create('posts-data', posts_processed)

    print('Done with processing posts')

    return stock_frequencies