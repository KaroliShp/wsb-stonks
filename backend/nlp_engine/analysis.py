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
from nltk.util import ngrams
import emoji
import regex


STOP_WORDS = set(stopwords.words('english'))
FORIBIDDEN_WORDS = set(read_foribidden_words())
STOCKS, COMPANIES = read_stocks()


# Stocks NLP analysis


def get_stock_frequency(posts):
    cleaned_posts = tokenize_posts_stocks(posts)

    frequency = {}
    #company_names_underscores = [ name.replace(" ", "_") for name in company_names]

    for post in cleaned_posts:
        #print(posts[cleaned_posts.index(post)])
        stocks_in_doc = set()

        # Find all mentioned stocks in a post
        for token in post:
            if token in STOCKS:
                stocks_in_doc.add(token.upper())
                #print(token.upper())
        
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
        # It's a post
        if 'title' in post:
            tokens = tknzr.tokenize(post['title']) + tknzr.tokenize(post['selftext'])
        # It's a comment
        else:
            tokens = tknzr.tokenize(post['body'])


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
    # 1-gram
    tokens_1 = tokenize_posts_keywords_1(posts)
    fdist_1 = FreqDist(tokens_1)
    top_keywords_1 = fdist_1.most_common(100)
    
    tokens_n = tokenize_posts_keywords_n(posts)

    # 2-gram
    bigrams = ngrams(tokens_n, 2)
    fdist_2 = FreqDist(bigrams)
    top_keywords_2 = fdist_2.most_common(100)
    top_keywords_2 = [(f'{keywords[0]} {keywords[1]}', mentions) for keywords, mentions in top_keywords_2]

    # 3-gram
    trigrams = ngrams(tokens_n, 3)
    fdist_3 = FreqDist(trigrams)
    top_keywords_3 = fdist_3.most_common(100)
    top_keywords_3 = [(f'{keywords[0]} {keywords[1]} {keywords[2]}', mentions) for keywords, mentions in top_keywords_3]

    top_keywords = top_keywords_1 + top_keywords_2 + top_keywords_3
    return [{ 'keyword' : keyword, 'mentions' : mentions } for keyword, mentions in top_keywords]


def tokenize_posts_keywords_1(posts):
    tokens_all = []

    for post in posts:
        # Tokenize the input
        tknzr = TweetTokenizer()
        # It's a post
        if 'title' in post:
            tokens = tknzr.tokenize(post['title']) + tknzr.tokenize(post['selftext'])
        # It's a comment
        else:
            tokens = tknzr.tokenize(post['body'])

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


def tokenize_posts_keywords_n(posts):
    tokens_all = []

    for post in posts:
        # Remove punctuation
        
        # It's a post
        if 'title' in post:
            post['title'] = re.sub('[^a-zA-Z]', ' ', post['title'])
            post['selftext'] = re.sub('[^a-zA-Z]', ' ', post['selftext'])

            # Remove special characters and digits
            post['title'] = re.sub("(\\d|\\W)+", " ", post['title'])
            post['selftext'] = re.sub("(\\d|\\W)+", " ", post['selftext'])
        # It's a comment
        else:
            post['body'] = re.sub('[^a-zA-Z]', ' ', post['body'])
            post['body'] = re.sub("(\\d|\\W)+", " ", post['body'])
        
        # Tokenize the input
        tknzr = TweetTokenizer()
        # It's a post
        if 'title' in post:
            tokens = tknzr.tokenize(post['title']) + tknzr.tokenize(post['selftext'])
        # It's a comment
        else:
            tokens = tknzr.tokenize(post['body'])

        # Remove tokens that are of length less than 2 or longer than 12
        tokens = list(filter(lambda x : len(x) >= 2 and len(x) < 12, tokens))

        # Lower all tokens
        tokens = list(map(lambda x : x.lower() , tokens))

        # Remove stopwords
        tokens = list(filter(lambda x : x not in STOP_WORDS, tokens))

        # Lemmatize tokens
        tokens = list(map(lambda x : WordNetLemmatizer().lemmatize(x, 'v'), tokens))

        tokens_all += tokens

    return tokens_all


# Emoji analysis


def get_top_emoji(posts):
    all_emoji = {}
    
    for post in posts:
        # Get text where we will look for emojis
        # It's a post
        if 'title' in post:
            text = post['title'] + '. ' + post['selftext']
        # It's a comment
        else:
            text = post['body']

        # Find emojis
        data = regex.findall(r'\X', text)
        #flags = regex.findall(u'[\U0001F1E6-\U0001F1FF]', text) 
        for word in data:
            if any(char in emoji.UNICODE_EMOJI for char in word):
                if word in all_emoji:
                    all_emoji[word] += 1
                else:
                    all_emoji[word] = 1
    
    # Convert structure
    all_emoji_list = []
    for e, m in all_emoji.items():
        all_emoji_list.append({ 'emoji' : e, 'mentions' : m })

    return all_emoji_list



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