from base64 import b64encode, b64decode


# Helper methods


def encode_data(item):
    return b64encode(item.encode('utf-8')).decode('utf-8')


def decode_data(item):
    return b64decode(item).decode('utf-8')


# Actual methods


def write_posts(db_client, data):
    db_client.delete_many('posts', {})

    for item in data:
        title = encode_data(item.title)
        score = encode_data(str(item.score))
        selftext = encode_data(item.selftext)
        created = encode_data(str(item.created))
        db_client.create('posts', { 'title' : title, 'score' : score, 'selftext' : selftext, 'created' : created })
    

def retrieve_posts(db_client):    
    data = []
    
    raw_data = db_client.find_all('posts', {})

    for item in raw_data:
        title = decode_data(item['title'])
        score = int(decode_data(item['score']))
        selftext = decode_data(item['selftext'])
        created = float(decode_data(item['created']))
        data.append([title, score, selftext, created])
    
    return data


def write_companies(db_client, data):
    db_client.delete_many('companies', {})

    for item in data:
        db_client.create('companies', { 'symbol' : item[0], 'security' : item[1] })


def retrieve_companies(db_client):
    symbol_data = set()
    security_data = set()
    
    raw_data = db_client.find_all('companies', {})

    for item in raw_data:
        symbol_data.add(item['symbol'].lower())
        security_data.add(item['security'].lower())
    
    return symbol_data, security_data


def write_frequency(db_client, data):
    db_client.delete_many('analysis-stock-frequency', {})

    for k, v in data.items():
        db_client.create('analysis-stock-frequency', { 'symbol' : k, 'security' : 'NaN', 'mentions' : v })

        