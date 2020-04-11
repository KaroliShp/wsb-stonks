from datetime import datetime, timedelta


def get_keywords_top(db_client):
    print(f'Start getting top keywords')

    # Get raw top for each update in DB
    last_day = datetime.now() - timedelta(hours=24, minutes=0)
    raw_data = db_client.find_all('posts-data', { 'date' : { "$gt" : last_day } })

    # Find keyword top
    top_keywords = {}
    for data in raw_data:
        for obj in data['keywords']:
            if obj['keyword'] in top_keywords:
                top_keywords[obj['keyword']] += obj['mentions']
            else:
                top_keywords[obj['keyword']] = obj['mentions']

    # Convert dictionary to list of tuples
    top_keywords_list = sorted([ { 'keyword' : k, 'mentions' : v } for k, v in top_keywords.items() ], key=lambda x : x['mentions'], reverse=True)

    print('Finish calculating top keywords')

    return top_keywords_list