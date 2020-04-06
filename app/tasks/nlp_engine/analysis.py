import nltk
nltk.data.path.append('./nltk_data/')
from nltk.corpus import stopwords
from app.tasks.nlp_engine.io import read_from_file
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import MWETokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re


STOP_WORDS = set(stopwords.words('english'))


def get_stock_frequency(cleaned_posts, symbols, company_names):
    frequency = {}

    symbols_lowered = [ symbol.lower() for symbol in symbols ]
    company_names_underscores = [ name.replace(" ", "_") for name in company_names]

    for post in cleaned_posts:
        stocks_in_doc = set()

        # Find all mentioned stocks in a post
        for token in post:
            if token in symbols_lowered:
                stocks_in_doc.add(token.upper())
            elif token in company_names_underscores:
                stocks_in_doc.add(symbols[company_names_underscores.index(token)].upper())

        # Add 1 to frequency of mentioned stocks
        for stock in stocks_in_doc:
            if stock in frequency:
                frequency[stock] += 1
            else:
                frequency[stock] = 1
    
    return {k: v for k, v in sorted(frequency.items(), key=lambda item: item[1], reverse=True)}


def tokenize_posts(posts):
    """
    Tokenize and clean input
    """
    cleaned_posts = []

    for post in posts:
        # Tokenize the input
        tknzr = TweetTokenizer()
        tokens = tknzr.tokenize(post[0]) + tknzr.tokenize(post[2])

        # Lower all tokens
        tokens = list(map(lambda x : x.lower() , tokens))

        # Remove tokens that are of length less than 3 or longer than 15
        tokens = list(filter(lambda x : len(x) >= 3 and len(x) < 15, tokens))

        # Remove numbers
        tokens = list(filter(lambda x : not is_num(x), tokens))

        # Remove stopwords
        tokens = list(filter(lambda x : x not in STOP_WORDS, tokens))

        cleaned_posts.append(tokens)

    return cleaned_posts


def tokenize_posts_mwe(cleaned_posts, company_names):
    """
    Merge custom tokens together
    """
    cleaned_posts_mwe = []
    
    tokenizer = MWETokenizer()

    for name in company_names:
        tokenizer.add_mwe(tuple(name.lower().split(' ')))
    
    tokenizer.add_mwe(('wall', 'street'))
    tokenizer.add_mwe(('wall', 'street', 'bets'))
    
    for tokens in cleaned_posts:
        cleaned_posts_mwe.append(tokenizer.tokenize(tokens))
    
    return cleaned_posts_mwe


def lemmatize_words(cleaned_posts):
    lemmatized_posts = []

    for post in cleaned_posts:
        lemmatized_posts.append([ WordNetLemmatizer().lemmatize(x, 'v') for x in post ])

    return lemmatized_posts


"""
def tag_pos_posts(cleaned_posts):
    tags = []

    for tokens in cleaned_posts:
        tag = nltk.pos_tag(tokens)
        tags.append(tag)

    return tags
"""

# Helper method

def is_num(string):
    try:
        int(string)
        return True
    except ValueError:
        pass
    try:
        float(string)
        return True
    except ValueError:
        return False