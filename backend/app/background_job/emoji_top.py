from datetime import datetime, timedelta


def get_emoji_top(db_client):
    print(f'Start getting top emoji')

    # Get raw top for each update in DB
    last_day = datetime.now() - timedelta(hours=24, minutes=0)
    raw_data = db_client.find_all('posts-data', { 'date' : { "$gt" : last_day } })

    # Find emojis top
    top_emoji = {}
    for data in raw_data:
        for obj in data['top_emoji']:
            if obj['emoji'] in top_emoji:
                top_emoji[obj['emoji']] += obj['mentions']
            else:
                top_emoji[obj['emoji']] = obj['mentions']

    # Convert dictionary to list of tuples
    top_emoji_list = sorted([ { 'emoji' : k, 'mentions' : v } for k, v in top_emoji.items() ], key=lambda x : x['mentions'], reverse=True)

    print('Finish calculating top emoji')

    return top_emoji_list