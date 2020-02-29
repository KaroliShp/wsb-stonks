import nltk
from nlp_engine.io import read_from_file, read_stocks


def get_stock_frequency(data, symbol_data, security_data):
    frequency = {}

    for item in data:
        # Store mentions of the post
        stocks_document = set()

        # Tokenize document and do some preprocessing
        tokens = nltk.word_tokenize(item[0]) + nltk.word_tokenize(item[2])
        tokens = list(filter(lambda x : len(x) >= 3 and len(x) < 15, tokens))

        # Find all mentioned stocks in a post
        for token in tokens:
            if token.lower() in symbol_data and token.isupper():
                stocks_document.add(token)
            elif token.lower() in security_data:
                stocks_document.add(token)

        # Add 1 to frequency of mentioned stocks
        for document in stocks_document:
            if document in frequency:
                frequency[document] += 1
            else:
                frequency[document] = 1
    
    return frequency
        


if __name__ == '__main__':
    data = read_from_file()
    symbol_data, security_data = read_stocks()

    print(get_stock_frequency(data, symbol_data, security_data))
