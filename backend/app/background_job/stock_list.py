def get_all_stocks(db_client):
    print(f'Start getting stock list')

    # Retrieve all stocks
    all_stocks = db_client.find_all('stock-frequency-historic', {})
    all_stocks = list(map(lambda x : { 'stock_name' : x['stock_name'].upper() }, all_stocks))

    db_client.delete_many('stock-list', {})
    db_client.create_many('stock-list', all_stocks)

    print('Finish getting stock list')