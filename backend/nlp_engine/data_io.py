def read_stocks():
    stocks = []

    with open('data/companylist.csv', 'r') as f:
        raw_data = f.readlines()

        for line in raw_data:
            items = line.split(',')
            symbol = items[0].strip()[1:-1]
            security = items[1].strip()[1:-1]
            stocks.append((symbol.lower(), security.lower()))

    return stocks


def read_foribidden_words():
    words = []

    with open('data/forbidden_words.txt', 'r') as f:
        raw_words = f.readlines()

        for line in raw_words:
            words.append(line.strip())
    
    return words


if __name__ == '__main__':
    print(read_stocks())
    print(read_foribidden_words())
