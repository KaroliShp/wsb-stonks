# Actual methods


def write_posts(db_client, data):
    db_client.delete_many('posts', {})

    for item in data:
        title = item.title
        score = str(item.score)
        selftext = item.selftext
        created = str(item.created)
        db_client.create('posts', { 'title' : title, 'score' : score, 'selftext' : selftext, 'created' : created })
    

def retrieve_posts(db_client):    
    data = []
    
    raw_data = db_client.find_all('posts', {})

    for item in raw_data:
        title = item['title']
        score = int(item['score'])
        selftext = item['selftext']
        created = float(item['created'])
        data.append([title, score, selftext, created])
    
    return data


def write_companies(db_client, data):
    db_client.delete_many('companies', {})

    for item in data:
        db_client.create('companies', { 'symbol' : item[0], 'security' : item[1] })


def retrieve_companies(db_client):
    symbol_data = []
    security_data = []
    
    raw_data = db_client.find_all('companies', {})

    for item in raw_data:
        symbol_data.append(item['symbol'])
        security_data.append(item['security'].strip())
    
    return symbol_data, security_data


def write_frequency(db_client, data):
    db_client.delete_many('analysis-stock-frequency', {})

    for k, v in data.items():
        db_client.create('analysis-stock-frequency', { 'symbol' : k, 'security' : 'NaN', 'mentions' : v })

        