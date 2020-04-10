from nlp_engine.analysis import get_stock_frequency, get_top_keywords, get_top_emoji
from copy import deepcopy


def process_posts(db_client, posts, update_date, comments):
    """
    Process posts by extracting information from raw posts such as keywords, stock mentions and put into DB
    """
    print(f'Start processing posts')

    posts_processed = {}
    posts_processed['date'] = update_date

    # Feed new posts into NLP engine to perform frequency calculations
    stock_frequencies = get_stock_frequency(deepcopy(posts) + deepcopy(comments))
    posts_processed = { **posts_processed, **stock_frequencies }

    # Feed new posts into NLP engine to perform keyword analysis
    top_keywords = { 'top_keywords' : get_top_keywords(deepcopy(posts) + deepcopy(comments)) }
    posts_processed = { **posts_processed, **top_keywords }

    # Feed new posts into NLP engine to perform emoji analysis
    top_emoji = { 'top_emoji' : get_top_emoji(deepcopy(posts) + deepcopy(comments)) }
    posts_processed = { **posts_processed, **top_emoji }

    print('Done with processing posts')

    return posts_processed