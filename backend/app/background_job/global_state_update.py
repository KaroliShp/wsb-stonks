def update_top_stocks(db_client, start_date, end_date):
    global_stocks = {}

    K = 24*2
    all_stocks = db_client.find_k_of('top-stocks', {}, sort_by="end_date", k=K, ascending=False)

    # Calculate all stock mentions
    for stocks in all_stocks:
        for stock in stocks['stocks']:
            if stock['stock_name'] in global_stocks:
                global_stocks[stock['stock_name']] += stock['mentions']
            else:
                global_stocks[stock['stock_name']] = stock['mentions']

    # Get top stocks
    global_stocks_top = []
    for stock in sorted(global_stocks.items(), key=lambda item: item[1], reverse=True):
        global_stocks_top.append({ 'stock_name' : stock[0], 'mentions' : stock[1] })

    return global_stocks_top


def update_top_emojis(db_client, start_date, end_date):
    global_emojis = {}

    K = 24*2
    all_emojis = db_client.find_k_of('top-emojis', {}, sort_by="end_date", k=K, ascending=False)

    # Calculate all emoji mentions
    for emojis in all_emojis:
        for emoji in emojis['emoji']:
            if emoji['emoji'] in global_emojis:
                global_emojis[emoji['emoji']] += emoji['mentions']
            else:
                global_emojis[emoji['emoji']] = emoji['mentions']

    # Get top emojis
    global_emojis_top = []
    for emoji in sorted(global_emojis.items(), key=lambda item: item[1], reverse=True):
        global_emojis_top.append({ 'emoji' : emoji[0], 'mentions' : emoji[1] })

    return global_emojis_top


def update_total_stats(db_client, start_date, end_date):
    K = 24*2
    all_stats = db_client.find_k_of('statistics', {}, sort_by="end_date", k=K, ascending=False)

    total_posts = 0
    total_comments = 0
    top_post_author = {}
    top_comments_author = {}
    top_poster = { 'user_name' : '', 'posts' : 0 }
    top_commenter = { 'user_name' : '', 'comments' : 0 }
    posts_activity = []
    comments_activity = []

    for stats in all_stats:
        total_posts += stats['total_posts']
        total_comments += stats['total_comments']

        posts_activity.append({ 'time' : stats['start_date'].strftime("%H:%M"), 'amount' : stats['total_posts'] })
        comments_activity.append({ 'time' : stats['start_date'].strftime("%H:%M"), 'amount' : stats['total_comments'] })

        for top_author, posts in stats['top_post_authors'].items():
            if top_author == 'AutoModerator':
                continue
            if top_author in top_post_author:
                top_post_author[top_author] += posts
            else:
                top_post_author[top_author] = posts

        for top_author, comments in stats['top_comments_author'].items():
            if top_author == 'AutoModerator':
                continue
            if top_author in top_comments_author:
                top_comments_author[top_author] += comments
            else:
                top_comments_author[top_author] = comments

    top_poster_tpl = sorted(top_post_author.items(), key=lambda item: item[1], reverse=True)[0]
    top_poster['user_name'] = top_poster_tpl[0]
    top_poster['posts'] = top_poster_tpl[1]

    top_commenter_tpl = sorted(top_comments_author.items(), key=lambda item: item[1], reverse=True)[0]
    top_commenter['user_name'] = top_commenter_tpl[0]
    top_commenter['comments'] = top_commenter_tpl[1]

    statistics = {}
    statistics['total_posts'] = total_posts
    statistics['total_comments'] = total_comments
    statistics['top_post_authors'] = top_post_author
    statistics['top_comments_author'] = top_comments_author
    statistics['last_update'] = start_date
    
    posts_activity.reverse()
    statistics['posts_activity'] = posts_activity
    comments_activity.reverse()
    statistics['comments_activity'] = comments_activity
    statistics['top_poster'] = top_poster
    statistics['top_commenter'] = top_commenter

    return statistics


def update_top_stocks_historic(db_client, start_date, end_date):
    K = 24*2
    top_stocks = db_client.find_k_of('top-stocks', {}, sort_by="end_date", k=K, ascending=False)
    
    # Get all mentioned stocks and all possible updates
    all_updates = []
    all_stocks = {}
    for raw_data in top_stocks:
        all_updates.append(raw_data['start_date'])
        for data in raw_data['stocks']:
            if data['stock_name'] in all_stocks:
                all_stocks[data['stock_name']] += [ { 'time' : raw_data['start_date'], 'amount' : data['mentions'] } ]
            else:
                all_stocks[data['stock_name']] = [ { 'time' : raw_data['start_date'], 'amount' : data['mentions'] } ]

    # Fill mention gaps - insert 0 mentions for where the dates are not available
    for stock, value in all_stocks.items():
        # Updates where the stock was mentioned (%Y-%m-%d %H:%M format)
        updates = set([data['time'].strftime("%Y-%m-%d %H:%M") for data in value])
        for expected_update in all_updates:
            if expected_update.strftime("%Y-%m-%d %H:%M") not in updates:
                all_stocks[stock] += [ { 'time' : expected_update, 'amount' : 0  } ]

    # Restructure data
    stocks = []
    for key, val in all_stocks.items():
        # Sort and change date representation to just %H:%M for website
        historic_data = sorted(val, key=lambda x : x['time'], reverse=True)
        historic_data = list(map(lambda x : { 'amount' : x['amount'], 'time' : x['time'].strftime("%H:%M") }, historic_data))
        stocks.append({
            'stock_name' : key,
            'historic_data' : historic_data
        })

    return stocks
