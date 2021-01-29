from nlp_engine.analysis import get_stock_frequency, get_top_keywords, get_top_emoji, get_top_keywords_pytextrank
from copy import deepcopy


def process_posts(db_client, new_entries, start_date, end_date,):
    """
    Process posts by extracting information from raw posts such as keywords, stock mentions and put into DB
    """
    print(f'\nStart processing posts')

    # Feed new posts into NLP engine to perform frequency calculations
    stock_frequencies = { 'stocks' : get_stock_frequency(deepcopy(new_entries)), 'start_date' : start_date, 'end_date' : end_date }

    top_keywords = get_top_keywords_pytextrank(deepcopy(new_entries))[:10]

    # Feed new posts into NLP engine to perform emoji analysis
    top_emoji = { 'emoji' : get_top_emoji(deepcopy(new_entries)), 'start_date' : start_date, 'end_date' : end_date }

    print('Done with processing posts\n')

    return stock_frequencies, top_emoji, top_keywords