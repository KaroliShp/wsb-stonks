def get_all_stocks(db_client):
    # print(f'Start getting stock list')

    # Retrieve all stocks
    all_stocks = db_client.find_all('top-stocks-historic', {})
    all_stocks = list(map(lambda x : { 'stock_name' : x['stock_name'].upper() }, all_stocks))

    # print('Finish getting stock list')

    return all_stocks