from nlp_engine.data_io import read_stocks, read_foribidden_words

import nltk
nltk.data.path.append('./nltk_data/')
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer
import re
from nltk import FreqDist
from nltk.util import ngrams
import emoji
import regex
import nltk.data
from collections import Counter
from nltk import tokenize
import string
from copy import deepcopy
from datetime import datetime, timedelta
import numpy as np
import spacy
import pytextrank
import math
import itertools


STOP_WORDS = set(stopwords.words('english'))
FORIBIDDEN_WORDS = set(read_foribidden_words())
STOCKS, COMPANIES = read_stocks()
STOCKS += [ 'vix', 'vxx', 'rope', 'gdx', 'trnp', 'uso', 'dia', 'iwm', 'gld', 'hyg', 'jnug', 'spxs', 'xle', 'fas', 'uso' ]
STOCKS = set(STOCKS)
EXTRA_STOCKS = [ 'gme', 'bb', 'nok', 'amc' ]

# Stocks NLP analysis


def get_stock_frequency(entries):
    """
    Get stock frequency from input posts for a specific date
    """
    stock_frequency = {}

    # Extract text for processing
    """
    raw_text = [] # raw text in sentences
    for post in posts:
        raw_text.append(post['title'])
        raw_text += tokenize.sent_tokenize(post['selftext'])
    for comment in comments:
        raw_text += tokenize.sent_tokenize(comment['body'])
    """

    raw_text = [] # raw text in sentences
    for entry in entries:
        # Its a post
        if 'title' in entry:
            raw_text.append(entry['title'])
            raw_text += tokenize.sent_tokenize(entry['selftext'])
        else:
            raw_text += tokenize.sent_tokenize(entry['body'])


    # First stage of text preprocessing
    cleaned_text = []
    for text in raw_text:
        text = text.lower() # Convert text to lowercase
        text = re.sub(r'http\S+', '', text) # Remove URLs
        text = re.sub(r"\d+%", '', text) # Remove percentage and integers before it
        text = re.sub(' +', ' ', text).strip() # Remove multiple spaces
        cleaned_text.append(text)

    """
    pattern_1 = r"(\b|\$)([a-z])+ (\d)+/(\d)+\b" # stock month/day
    pattern_2 = r"((buy)|(sell)|(short)|(long)) \$?([a-z])+" # buy/sell/short/long
    pattern_3 = r"\$[a-z]+\b" # $SPY
    pattern_4 = r"(\b|\$)([a-z])+ \$?(\d)+(p|c|\$)\b" # stock price
    """

    pattern_x_1 = r"(\b|\$)([a-z])+(\b|\$)"
    pattern_x_2 = r"\b(\d)+/(\d)+\b"
    pattern_x_3 = r"(\b|\$)(\d)+([a-z]|\$|\b)*"

    pattern_1_list = []
    for pattern in list(itertools.permutations([pattern_x_1, pattern_x_2])):
        pattern_1 = r'(' + r' '.join(pattern) + r')'
        pattern_1_list.append(pattern_1)
    pattern_1 = r'|'.join(pattern_1_list)

    pattern_4_list = []
    for pattern in list(itertools.permutations([pattern_x_1, pattern_x_3])):
        pattern_4 = r'(' + r' '.join(pattern) + r')'
        pattern_4_list.append(pattern_4)
    pattern_4 = r'|'.join(pattern_4_list)

    pattern_5_list = []
    for pattern in list(itertools.permutations([pattern_x_1, pattern_x_2, pattern_x_3])):
        pattern_5 = r'(' + r' '.join(pattern) + r')'
        pattern_5_list.append(pattern_5)
    pattern_5 = r'|'.join(pattern_5_list)

    verbs = [ 'buy', 'buys', 'bought', 'buying', 'sell', 'sells', 'sold', 'selling', 'short', 'shorts', 'shorted', 'long', 'longed', 'longs', 'hold', 'held' ]
    verbs = [ f'({v})' for v in verbs ]
    verbs_regex = '|'.join(verbs)
    pattern_2 = r"(" + verbs_regex + r") \$?([a-z])+ ((calls)|(puts)|(call)|(put))?" # buy/sell/short/long

    pattern_3 = r"\$[a-z]+\b" # $SPY

    pattern_6 = r"(\b|\$)([a-z])+(\b|\$) ((calls)|(puts)|(call)|(put))"

    # Extract stocks mentioned in specific formats
    for text in cleaned_text:
        candidate_stocks = {}
        to_print = text

        # Match pattern 5 and remove it from the sentence
        while True:
            res_5 = re.search(pattern_5, text)
            if not (res_5 is None):
                stock = res_5.group().split(' ')[0]
                text = re.sub(' +', ' ', text.replace(res_5.group(), "")).strip()
                candidate_stocks[stock] = 5
            else:
                break
            
        # Match pattern 2 and remove it from the sentence
        while True:
            res_2 = re.search(pattern_2, text)
            if not (res_2 is None):
                stock = res_2.group().split(' ')[1]
                if stock not in STOP_WORDS:
                    text = re.sub(' +', ' ', text.replace(res_2.group(), "")).strip()
                    candidate_stocks[stock] = 2
                else:
                    break
            else:
                break
            
        # Pattern 1
        while True:
            res_1 = re.search(pattern_1, text)
            if not (res_1 is None):
                stock = res_1.group().split(' ')[0]
                text = re.sub(' +', ' ', text.replace(res_1.group(), "")).strip()
                candidate_stocks[stock] = 1
            else:
                break

        # Pattern 6
        while True:
            res_6 = re.search(pattern_6, text)
            if not (res_6 is None):
                stock = res_6.group().split(' ')[0]
                text = re.sub(' +', ' ', text.replace(res_6.group(), "")).strip()
                candidate_stocks[stock] = 6
            else:
                break

        # Pattern 4
        while True:
            res_4 = re.search(pattern_4, text)
            if not (res_4 is None):
                stock = res_4.group().split(' ')[0]
                text = re.sub(' +', ' ', text.replace(res_4.group(), "")).strip()
                candidate_stocks[stock] = 4
            else:
                break

        # Match pattern 3 and remove it from the sentence
        res_3 = re.findall(pattern_3, text)
        if len(res_3) > 0:
            stocks = dict(Counter(res_3))
            for stock, _ in stocks.items():
                text = re.sub(' +', ' ', text.replace(stock, "")).strip()
                candidate_stocks[stock[1:]] = 3

        # Add stock frequency
        if len(candidate_stocks) > 0:
            #print(to_print)
            pass
        for stock, p in candidate_stocks.items():
            if stock[0] == '$' or stock[-1] == '$':
                stock = stock[1:]
            if stock in STOCKS and stock not in FORIBIDDEN_WORDS:
                #print(to_print)
                #print(f'({p}) {stock}')
                #print('\n')
                if stock in stock_frequency:
                    stock_frequency[stock] += 1
                else:
                    stock_frequency[stock] = 1
            else:
                #print(f'- ({p}) {stock}')
                pass
            #print('\n')

    # Restructure and return
    return [ { 'stock_name' : k.upper(), 'mentions' : v } for k, v in stock_frequency.items() ]


# Top keyword NLP analysis


def get_top_keywords(entries):
    # Extract text for processing
    """
    raw_text = [] # raw text in sentences
    for post in posts:
        raw_text.append(post['title'])
        raw_text += tokenize.sent_tokenize(post['selftext'])
    for comment in comments:
        raw_text += tokenize.sent_tokenize(comment['body'])
    """

    raw_text = [] # raw text in sentences
    for entry in entries:
        # Its a post
        if 'title' in entry:
            raw_text.append(entry['title'])
            raw_text += tokenize.sent_tokenize(entry['selftext'])
        else:
            raw_text += tokenize.sent_tokenize(entry['body'])
    
    # Tokenize
    tokens = tokenize_posts_keywords(raw_text)

    # 1-gram
    fdist_1 = FreqDist(tokens)
    top_keywords_1 = fdist_1.most_common(100)
    
    # 2-gram
    bigrams = ngrams(tokens, 2)
    fdist_2 = FreqDist(bigrams)
    top_keywords_2 = fdist_2.most_common(100)
    top_keywords_2 = [(f'{keywords[0]} {keywords[1]}', mentions) for keywords, mentions in top_keywords_2]

    # 3-gram
    trigrams = ngrams(tokens, 3)
    fdist_3 = FreqDist(trigrams)
    top_keywords_3 = fdist_3.most_common(100)
    top_keywords_3 = [(f'{keywords[0]} {keywords[1]} {keywords[2]}', mentions) for keywords, mentions in top_keywords_3]

    top_keywords = top_keywords_1 + top_keywords_2 + top_keywords_3
    return [{ 'keyword' : keyword, 'mentions' : mentions } for keyword, mentions in top_keywords]


def get_top_keywords_all_ngrams(new_entries_by_date):
    # Get the raw text (sentences)
    raw_text = []
    for date, new_entries in new_entries_by_date.items():
        for post in deepcopy(new_entries['posts']):
            raw_text.append(post['title'])
            raw_text += tokenize.sent_tokenize(post['selftext'])
        for comment in deepcopy(new_entries['comments']):
            raw_text += tokenize.sent_tokenize(comment['body'])

    # Preprocess a bit
    cleaned_text = []
    for text in raw_text:
        text = text.lower() # Convert text to lowercase
        text = re.sub(r'http\S+', '', text) # Remove URLs
        text = re.sub(r"[^\w\s]", '', text) # Remove numbers and special characters
        text = re.sub(' +', ' ', text).strip() # Remove multiple spaces
        cleaned_text.append(text)

    # Tokens
    tokens_all = []
    tknzr = TweetTokenizer()
    for text in cleaned_text:
        tokens = tknzr.tokenize(text)

        # Remove stopwords
        tokens = list(filter(lambda x : x not in STOP_WORDS, tokens))

        # Lemmatize tokens
        tokens = list(map(lambda x : WordNetLemmatizer().lemmatize(x, 'v'), tokens))

        tokens_all.append(tokens)

    # Ngrams popularity
    keywords = {}
    for tokens in tokens_all:
        fdist_1 = dict(FreqDist(deepcopy(tokens))) # 1-gram
        fdist_2 = dict(FreqDist(ngrams(deepcopy(tokens), 2))) # 2-gram
        fdist_3 = dict(FreqDist(ngrams(deepcopy(tokens), 3))) # 3-gram

        # Calculate frequency
        for fdist in [fdist_1, fdist_2, fdist_3]:
            for key, val in fdist.items():
                if key in keywords:
                    keywords[key] += val
                else:
                    keywords[key] = val
    
    # Normalize ngrams
    normalized_keywords = {}
    values = list(keywords.values())
    values_mean = np.mean(values)
    values_max = np.max(values)
    values_min = np.min(values)
    for key, val in keywords.items():
        normalized_keywords[key] = (val - values_mean) / ( values_max - values_min )

    most_common = [ (key, val) for key, val in sorted(keywords.items(), key=lambda x : x[1], reverse=True) ]
    #print(most_common[:100])
    return most_common


def get_top_keywords_pytextrank(entries):
    # Get the raw text (sentences)
    """ 
    raw_text = []
    for date, new_entries in new_entries_by_date.items():
        for post in deepcopy(new_entries['posts']):
            raw_text.append(post['title'])
            raw_text += tokenize.sent_tokenize(post['selftext'])
        for comment in deepcopy(new_entries['comments']):
            raw_text += tokenize.sent_tokenize(comment['body'])
    """ 
    raw_text = [] # raw text in sentences
    for entry in entries:
        # Its a post
        if 'title' in entry:
            raw_text.append(entry['title'])
            raw_text += tokenize.sent_tokenize(entry['selftext'])
        else:
            raw_text += tokenize.sent_tokenize(entry['body'])

    # Preprocess and calculate keywords per 100000 characters
    global_ranks = {}
    global_ranks_mentions = {}
    cleaned_text = ""
    for c, text in enumerate(raw_text):
        text = text.lower() # Convert text to lowercase
        text = re.sub(r'http\S+', '', text) # Remove URLs
        text = re.sub(' +', ' ', text).strip() # Remove multiple spaces
        cleaned_text += f'{text}. '

        if len(cleaned_text) >= 90000 or c == (len(raw_text) - 1):
            nlp = spacy.load("en_core_web_sm")
            nlp.add_pipe("textrank", name="textrank", last=True)
            doc = nlp(cleaned_text)
            for c, r in enumerate(doc._.phrases):
                if r.text in global_ranks:
                    global_ranks[r.text] = max(r.rank, global_ranks[r.text])
                    global_ranks_mentions[r.text] += r.count
                else:
                    global_ranks[r.text] = r.rank
                    global_ranks_mentions[r.text] = r.count
            cleaned_text = ""

    # Finish
    """
    for r in global_ranks.keys():
        global_ranks[r] = np.mean(global_ranks[r])
    """
    keywords_rank = sorted(global_ranks.items(), key=lambda x : x[1], reverse=True)

    # Ranking
    top_keywords = []
    for k, v in keywords_rank:
        # Choose a random threshold
        if global_ranks_mentions[k] < 5:
            continue
        #print(f'{k} {global_ranks_mentions[k]} {v}')
        top_keywords.append({ 'keyword' : k, 'mentions' : v })
        if len(top_keywords) == 10:
            break

    return top_keywords


def tokenize_posts_keywords(raw_text):
    # Preprocess whole text
    cleaned_text = []
    for text in raw_text:
        text = text.lower() # Convert text to lowercase
        text = re.sub(r'http\S+', '', text) # Remove URLs
        text = re.sub(r"[^\w\s]", '', text) # Remove numbers and special characters
        text = re.sub(' +', ' ', text).strip() # Remove multiple spaces
        cleaned_text.append(text)

    # Tokenize to words
    tokens_all = []
    tknzr = TweetTokenizer()
    for text in cleaned_text:
        tokens = tknzr.tokenize(text)

        # Remove stopwords
        tokens = list(filter(lambda x : x not in STOP_WORDS, tokens))

        # Lemmatize tokens
        tokens = list(map(lambda x : WordNetLemmatizer().lemmatize(x, 'v'), tokens))

        tokens_all += tokens

    return tokens_all


# Emoji analysis


def get_top_emoji(posts):
    """
    Get top emoji from given posts
    """
    all_emoji = {}
    
    for post in posts:
        # Get text where we will look for emojis
        if 'title' in post:
            text = post['title'] + '. ' + post['selftext']  # It's a post
        else:
            text = post['body']  # It's a comment

        # Find emojis
        data = regex.findall(r'\X', text)
        #flags = regex.findall(u'[\U0001F1E6-\U0001F1FF]', text) 
        for word in data:
            if emoji.is_emoji(word):
                if word in all_emoji:
                    all_emoji[word] += 1
                else:
                    all_emoji[word] = 1
    
    # Convert structure
    all_emoji_list = []
    for e, m in all_emoji.items():
        all_emoji_list.append({ 'emoji' : e, 'mentions' : m })

    return all_emoji_list


if __name__ == '__main__':
    new_entries_by_date = {
        datetime(2020, 4, 11, 7, 18, 7): {
            'posts': [
                {
                    'title': 'What if we just start our own Federal Reserve Bank?', 
                    'score': 1, 
                    'selftext': 'I was doing some DD and came across these 2 legal cases:  \n\n\n In *United States Shipping Board Emergency Fleet Corporation v. Western Union Telegraph Co.*,[\\[5\\]](https://en.wikipedia.org/wiki/Federal_Reserve_Bank#cite_note-5) the U.S. Supreme Court stated, "Instrumentalities like the national banks or the federal reserve banks, in which there are private interests, are not departments of the government. They are private corporations in which the government has an interest." \n\nand\n\n In *Lewis v. United States*,[\\[7\\]](https://en.wikipedia.org/wiki/Federal_Reserve_Bank#cite_note-Lewis-vs-U.S.-7) the [United States Court of Appeals for the Ninth Circuit](https://en.wikipedia.org/wiki/United_States_Court_of_Appeals_for_the_Ninth_Circuit) stated that: "The Reserve Banks are not federal instrumentalities for purposes of the FTCA \\[the [Federal Tort Claims Act](https://en.wikipedia.org/wiki/Federal_Tort_Claims_Act)\\], but are independent, privately owned and locally controlled corporations."   \n\n\nSo since the Federal Reserve is a private corporation and doesn\'t seem to have a copyright to the name (since there are already 12 of these things). What if we just start our own? Then we can buy one of those brand new money printers everyone talks so much about instead of wasting our money on puts!  \n\n\nTLDR: Federal reserve is a private company. Start our own Federal Reserve of WSB. Purchase money printer. Profit???', 
                    'created': datetime(2020, 4, 11, 7, 18, 5), 
                    'author': 'wannabecameraguy', 
                    'num_comments': 0, 
                    'url': 'https://www.reddit.com/r/wallstreetbets/comments/fyyxc9/what_if_we_just_start_our_own_federal_reserve_bank/'
                }, {
                    'title': "JPow doesn't need to stop the economy from crashing to fuck over your puts", 
                    'score': 1, 
                    'selftext': "I tried to post this 2 weeks ago, but automod deleted the post :/ The advice is still important though.\n\nYou're right, the fed can't save the economy from going tits up. Printing money obviously doesn't cure the beer flu, but you know what it does do? Artificially inflate asset prices.\n\n**YOUR PUTS ARE NOT FUCKING SAFE: Puts are bets that the NOMINAL price of stocks will go down, but the REAL value of stocks going down doesn't necessarily mean that their nominal price will go down.**\n\nJP has already started flooding the economy with trillions of dollars. Do you REALLY think Trump is just gonna let him stop, especially in an election year? NO, we are going to have stagflation.\n\nThat doesn't mean you can't make some money on puts in the short run, but it DOES mean that **you need to be careful to not overestimate how far you think the market will fall because inflation will be working against you.**\n\nTo the autists out here who still don't get it, here's a picture with pretty lines to show you what I'm talking about. After Nixon took us off the gold standard in 1971 we went through a period of heavy inflation. Over the next decade, the real value of the DJIA (pretty red line) lost over 60% of its value before it bottomed out in 1982. Meanwhile, the nominal price of the DJIA (pretty blue line) bottomed out in 1974 and quickly recouped its losses. Even though the economy was weak for a decade, puts weren't printing.\n\nhttps://preview.redd.it/afksv9jp15s41.png?width=538&format=png&auto=webp&s=40493a649a6ce3059e04c3b814ecb6d2d9932ffe", 
                    'created': datetime(2020, 4, 11, 7, 16, 5), 
                    'author': 'HelloFromTheSexySide', 
                    'num_comments': 0, 
                    'url': 'https://www.reddit.com/r/wallstreetbets/comments/fyyw1u/jpow_doesnt_need_to_stop_the_economy_from/'
                }, {
                    'title': 'Week of opportunities', 
                    'score': 2, 
                    'selftext': 'Msft 9/18 $170c. Tsla 5/15 $770cs.                                Ba 5/15 $200c or 8/21 $255c  Jpm  5/15 $115c.      V 5/15 $185cs Oled 5/15 $85ps. Sq 5/2 $52p   Gild 8/21 87.5c. Sqqq 5/15 $24cs Weekly $Spy 254ps.\n\nThoughts on entering these positions?', 
                    'created': datetime(2020, 4, 11, 7, 12, 33), 
                    'author': 'Apdvadar', 
                    'num_comments': 3, 
                    'url': 'https://www.reddit.com/r/wallstreetbets/comments/fyytvm/week_of_opportunities/'
                }, {
                    'title': 'VS is 🌈🐻 Messiah', 
                    'score': 3, 
                    'selftext': 'Do you not see? Do you not understand? Throw out your shitty TA and fundamentals bullshit for the prophecy is nearly fulfilled. \n\nOur 🌈🐻 messiah, u/Variation-Separate, went long and sacrificed his puts so that ours may be redeemed. He will rise 🌈🐻 again on the next trading day and all will see that he spoke the truth.\n\nThose who abandoned him and mocked him during the great trial and tribulation shall be forgiven should they repent their bullish ways. For VS brings tendies to all who believe. First for the 🌈🐻 then for the 🐂.\n\nEdit: I am a true disciple - SPY 4/22 250p, 5/15 210p, 6/19 190p, 9/18 240p', 
                    'created': datetime(2020, 4, 11, 6, 54, 52), 
                    'author': 'TheBritz', 
                    'num_comments': 3, 
                    'url': 'https://www.reddit.com/r/wallstreetbets/comments/fyyild/vs_is_messiah/'}
            ], 'comments': [
                {
                    'body': 'Inverse em all', 
                    'author': 'KDdoingnumbers', 
                    'created': datetime(2020, 4, 11, 7, 14, 3), 
                    'url': '/r/wallstreetbets/comments/fyytvm/week_of_opportunities/fn2hjm7/'
                }, {
                    'body': 'Spy is not dropping. Ban this idiot.', 
                    'author': 'HHMVP1', 
                    'created': datetime(2020, 4, 11, 7, 15, 10), 
                    'url': '/r/wallstreetbets/comments/fyytvm/week_of_opportunities/fn2hlxt/'
                }, {
                    'body': 'Did you just say MSFT calls and SPY puts? Hurd you', 
                    'author': 'Sinclister', 
                    'created': datetime(2020, 4, 11, 7, 17, 12), 
                    'url': '/r/wallstreetbets/comments/fyytvm/week_of_opportunities/fn2hq77/'
                }, {
                    'body': 'I’m VS gang all the way but god damn this post is stupid as fuck. \n\nBan', 
                    'author': '14HartmanA', 
                    'created': datetime(2020, 4, 11, 6, 59, 14), 
                    'url': '/r/wallstreetbets/comments/fyyild/vs_is_messiah/fn2goh7/'
                }, {
                    'body': 'When he appears to us he will show us the scars in his portfolio and in his savings and we will know it is him.', 
                    'author': 'TheBritz', 
                    'created': datetime(2020, 4, 11, 6, 56, 15), 
                    'url': '/r/wallstreetbets/comments/fyyild/vs_is_messiah/fn2gi37/'
                }, {
                    'body': 'VS bless', 
                    'author': 'TheBritz', 
                    'created': datetime(2020, 4, 11, 7, 4, 6), 
                    'url': '/r/wallstreetbets/comments/fyyild/vs_is_messiah/fn2gyt0/'
                }
            ]
        }
    }

    get_stock_frequency(new_entries_by_date[datetime(2020, 4, 11, 7, 18, 7)])
    get_top_keywords_pytextrank(new_entries_by_date)
