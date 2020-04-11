from nlp_engine.analysis import get_stock_frequency, get_top_keywords, get_top_emoji
from copy import deepcopy


def process_posts(db_client, new_entries, update_date):
    """
    Process posts by extracting information from raw posts such as keywords, stock mentions and put into DB
    """
    print(f'Start processing posts')

    posts_processed = {}
    posts_processed['date'] = update_date

    # Feed new posts into NLP engine to perform frequency calculations
    stock_frequencies = { 'stocks' : get_stock_frequency(deepcopy(new_entries['posts']) + deepcopy(new_entries['comments'])) }
    posts_processed = { **posts_processed, **stock_frequencies }

    # Feed new posts into NLP engine to perform keyword analysis
    top_keywords = { 'keywords' : get_top_keywords(deepcopy(new_entries['posts']) + deepcopy(new_entries['comments'])) }
    posts_processed = { **posts_processed, **top_keywords }

    # Feed new posts into NLP engine to perform emoji analysis
    top_emoji = { 'emoji' : get_top_emoji(deepcopy(new_entries['posts']) + deepcopy(new_entries['comments'])) }
    posts_processed = { **posts_processed, **top_emoji }

    print('Done with processing posts')

    return posts_processed