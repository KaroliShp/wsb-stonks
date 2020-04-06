from base64 import b64encode, b64decode


# Helper methods


def encode_data(item):
    return b64encode(item.encode('utf-8')).decode('utf-8')


def decode_data(item):
    return b64decode(item).decode('utf-8')


# Actual methods


def write_to_file(data):
    with open('data.csv', 'w') as f:
        for item in data:
            title = encode_data(item.title)
            score = encode_data(str(item.score)) # b64encode(bytes(str(item.score), encoding='utf-8')).decode('utf-8')
            selftext = encode_data(item.selftext)
            created = encode_data(str(item.created))
            f.write(f'{title},{score},{selftext},{created}\n')


def read_from_file():
    data = []

    with open('data.csv', 'r') as f:
        raw_data = f.readlines()

        for line in raw_data:
            items = line.split(',')
            title = decode_data(items[0])
            score = int(decode_data(items[1]))
            selftext = decode_data(items[2])
            created = float(decode_data(items[3]))
            data.append({'title' : title, 'score' : score, 'selftext' : selftext, 'created' : created})
    
    return data


def read_stocks():
    data = []

    with open('app/tasks/nlp_engine/company_list.csv', 'r') as f:
        raw_data = f.readlines()

        for line in raw_data:
            items = line.split(',')
            symbol = items[0]
            security = items[1].strip()
            data.append((symbol.lower(), security.lower()))
    
    return data