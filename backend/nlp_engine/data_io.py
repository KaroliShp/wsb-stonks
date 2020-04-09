def read_stocks():
    stocks_set = set()
    companies_set = set()

    for company_list in ["companylist_amex.csv", "companylist_nasdaq.csv", "companylist_nyse.csv"]:
        with open(f'data/{company_list}', 'r') as f:
            raw_data = f.readlines()

            for line in raw_data:
                items = line.split(',')
                symbol = items[0].strip()[1:-1]
                stocks_set.add(symbol.lower())

    return list(stocks_set), list(companies_set)


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
