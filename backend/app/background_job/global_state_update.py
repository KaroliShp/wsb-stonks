def update_top_stocks(db_client):
    global_stocks = {}

    all_stocks = db_client.find_all('top-stocks', {})
    print(all_stocks)

    # Calculate all stock mentions
    for stocks in all_stocks:
        for stock in stocks['stocks']:
            if stock['stock_name'] in global_stocks:
                global_stocks[stock['stock_name']] += stock['mentions']
            else:
                global_stocks[stock['stock_name']] = stock['mentions']

    # Get top stocks
    global_stocks_top = []
    for stock in sorted(global_stocks.items(), key=lambda item: item[1]):
        global_stocks_top.append({ 'stock_name' : stock[0], 'mentions' : stock[1] })
    print(global_stocks_top)

    return global_stocks_top


def update_top_emojis(db_client):
    global_emojis = {}

    all_emojis = db_client.find_all('top-emojis', {})
    print(all_emojis)

    # Calculate all emoji mentions
    for emojis in all_emojis:
        for emoji in emojis['emoji']:
            if emoji['emoji'] in global_emojis:
                global_emojis[emoji['emoji']] += emoji['mentions']
            else:
                global_emojis[emoji['emoji']] = emoji['mentions']

    # Get top emojis
    global_emojis_top = []
    for emoji in sorted(global_emojis.items(), key=lambda item: item[1]):
        global_emojis_top.append({ 'emoji' : emoji[0], 'mentions' : emoji[1] })
    print(global_emojis_top)

    return global_emojis_top


def update_total_stats(db_client, last_update):
    all_stats = db_client.find_all('statistics', {})
    print(all_stats)

    total_posts = 0
    total_comments = 0
    top_post_author = {}
    top_comments_author = {}

    for stats in all_stats:
        total_posts += stats['total_posts']
        total_comments += stats['total_comments']

        for top_author, posts in stats['top_post_authors'].items():
            if top_author in top_post_author:
                top_post_author[top_author] += posts
            else:
                top_post_author[top_author] = posts

        for top_author, comments in stats['top_comments_author'].items():
            if top_author in top_comments_author:
                top_comments_author[top_author] += comments
            else:
                top_comments_author[top_author] = comments

    statistics = {}
    statistics['total_posts'] = total_posts
    statistics['total_comments'] = total_comments
    statistics['top_post_authors'] = top_post_author
    statistics['top_comments_author'] = top_comments_author
    statistics['last_update'] = last_update

    print(statistics)

    return statistics
