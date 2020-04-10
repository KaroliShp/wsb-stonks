from datetime import datetime, timedelta
import math

import praw


CLIENT_ID = '2ocFsBoC1x3Ikw'
CLIENT_SECRET = 'j2CbxQJb53NFdqANAM60p1xCbt4'
USER_AGENT = 'wsb-stonks'
SUBREDDIT_NAME = 'wallstreetbets'


def fetch_posts(db_client, update_date, num_of_updates, limit):
    """ 
    Fetch the newest raw posts from subreddit given last update time
    :param db_client:
    """
    # Calculate last update time
    last_update = update_date - timedelta(hours=num_of_updates)

    print(f'Start fetching, current update: {update_date.strftime("%Y-%m-%d %H:%M:%S")}; last update: {last_update.strftime("%Y-%m-%d %H:%M:%S")}')

    # Authenticate with reddit API
    reddit_api = praw.Reddit(client_id=CLIENT_ID,
                             client_secret=CLIENT_SECRET,
                             user_agent=USER_AGENT)

    # Get the last posts that may contain duplicate posts
    last_posts = reddit_api.subreddit(SUBREDDIT_NAME).new(limit=limit)
    
    # Filter out only those posts that only belong to our earliest update date
    new_posts = [
        { 
            'title' : post.title, 
            'score' : post.score, 
            'selftext' : post.selftext, 
            'created' : datetime.utcfromtimestamp(post.created).replace(microsecond=0),
            'num_comments' : post.num_comments,
            'comments' : post,
            'author' : post.author.name
        } for post in last_posts if datetime.utcfromtimestamp(post.created) > last_update ]

    # Extend comments and append properly to the post information
    for post in new_posts:
        post['comments'].comments.replace_more(limit=0)
        all_comments = []
        for comment in  post['comments'].comments.list():
            all_comments.append(comment.body)
        post['comments'] = all_comments

    # Get all update dates for the number of updates inputed
    new_posts_by_date = {}
    for i in range(0, num_of_updates):
        new_posts_by_date[update_date - timedelta(hours=i)] = []

    # Group posts into batches based on their creation date
    for post in new_posts:
        update_diff = math.floor(((update_date - post['created']).total_seconds() / 3600))
        new_posts_by_date[update_date - timedelta(hours=update_diff)].append(post)

    print(f'Done fetching. Number of new posts: {len(new_posts)}')

    return new_posts_by_date
