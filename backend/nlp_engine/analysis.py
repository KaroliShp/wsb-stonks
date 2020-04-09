from nlp_engine.data_io import read_stocks, read_foribidden_words

import nltk
nltk.data.path.append('./nltk_data/')
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import MWETokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re
from nltk import FreqDist


STOP_WORDS = set(stopwords.words('english'))
FORIBIDDEN_WORDS = set(read_foribidden_words())
STOCKS = read_stocks()


# Stocks NLP analysis


def get_stock_frequency(posts):
    cleaned_posts = tokenize_posts_stocks(posts)

    frequency = {}

    symbols = list(map(lambda x : x[0], STOCKS))
    security_names = list(map(lambda x : x[1], STOCKS))
    #company_names_underscores = [ name.replace(" ", "_") for name in company_names]

    for post in cleaned_posts:
        stocks_in_doc = set()

        # Find all mentioned stocks in a post
        for token in post:
            if token in symbols:
                stocks_in_doc.add(token.upper())
        
        # Add 1 to frequency of mentioned stocks (mention once per post)
        for stock in stocks_in_doc:
            if stock in frequency:
                frequency[stock] += 1
            else:
                frequency[stock] = 1
    
    return {k: v for k, v in sorted(frequency.items(), key=lambda item: item[1], reverse=True)}


def tokenize_posts_stocks(posts):
    cleaned_posts = []

    for post in posts:
        # Tokenize the input
        tknzr = TweetTokenizer()
        tokens = tknzr.tokenize(post['title']) + tknzr.tokenize(post['selftext'])

        # Lower all tokens
        tokens = list(map(lambda x : x.lower() , tokens))

        # Remove tokens that are of length less than 3 or longer than 6
        tokens = list(filter(lambda x : len(x) >= 3 and len(x) < 6, tokens))

        # Remove numbers
        tokens = list(filter(lambda x : not is_num(x), tokens))

        # Remove stopwords
        tokens = list(filter(lambda x : x not in STOP_WORDS, tokens))

        # Remove foribidden words
        tokens = list(filter(lambda x : x not in FORIBIDDEN_WORDS, tokens))

        cleaned_posts.append(tokens)

    return cleaned_posts


# Top keyword NLP analysis


def get_top_keywords(posts):
    tokens = tokenize_posts_keywords(posts)
    fdist = FreqDist(tokens)
    top_keywords = fdist.most_common(10)
    return [{ 'keyword' : keyword, 'mentions' : mentions } for keyword, mentions in top_keywords]


def tokenize_posts_keywords(posts):
    tokens_all = []

    for post in posts:
        # Tokenize the input
        tknzr = TweetTokenizer()
        tokens = tknzr.tokenize(post['title']) + tknzr.tokenize(post['selftext'])

        # Lower all tokens
        tokens = list(map(lambda x : x.lower() , tokens))

        # Remove tokens that are of length less than 3 or longer than 12
        tokens = list(filter(lambda x : len(x) >= 3 and len(x) < 12, tokens))

        # Remove numbers
        tokens = list(filter(lambda x : not is_num(x), tokens))

        # Remove stopwords
        tokens = list(filter(lambda x : x not in STOP_WORDS, tokens))

        # Remove foribidden words
        tokens = list(filter(lambda x : x not in FORIBIDDEN_WORDS, tokens))

        # Lemmatize tokens
        tokens = list(map(lambda x : WordNetLemmatizer().lemmatize(x, 'v'), tokens))

        tokens_all += tokens

    return tokens_all


"""
def tokenize_posts_mwe(cleaned_posts, company_names):
    cleaned_posts_mwe = []
    
    tokenizer = MWETokenizer()

    for name in company_names:
        tokenizer.add_mwe(tuple(name.lower().split(' ')))
    
    tokenizer.add_mwe(('wall', 'street'))
    tokenizer.add_mwe(('wall', 'street', 'bets'))
    
    for tokens in cleaned_posts:
        cleaned_posts_mwe.append(tokenizer.tokenize(tokens))
    
    return cleaned_posts_mwe
"""

"""
def lemmatize_words(cleaned_posts):
    lemmatized_posts = []

    for post in cleaned_posts:
        lemmatized_posts.append([ WordNetLemmatizer().lemmatize(x, 'v') for x in post ])

    return lemmatized_posts
"""

"""
def tag_pos_posts(cleaned_posts):
    tags = []

    for tokens in cleaned_posts:
        tag = nltk.pos_tag(tokens)
        tags.append(tag)

    return tags
"""

# Helper methods

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


def get_stocks():
    return STOCKS