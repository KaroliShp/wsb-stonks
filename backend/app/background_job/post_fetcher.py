from datetime import datetime, timedelta

import praw


CLIENT_ID = '2ocFsBoC1x3Ikw'
CLIENT_SECRET = 'j2CbxQJb53NFdqANAM60p1xCbt4'
USER_AGENT = 'wsb-stonks'
SUBREDDIT_NAME = 'options'
POST_LIMIT = 200  # Assume that this is the upper limit of how many posts appear per update interval


def fetch_posts(db_client, last_update = datetime.now() - timedelta(hours=0, minutes=30)):
    """ 
    Fetch last 24 hrs posts from subreddit and store in the DB
    :param db_client:
    :param last_update_hrs: hours between consecutive post fetches
    :param last_update_minutes: minutes between consecutive post fetches
    """
    print(f'Start fetching, last update: {last_update.strftime("%Y-%m-%d %H:%M:%S")}')

    # Authenticate with reddit API
    reddit_api = praw.Reddit(client_id=CLIENT_ID,
                             client_secret=CLIENT_SECRET,
                             user_agent=USER_AGENT)

    # Get the last posts that may contain duplicate posts
    last_posts = reddit_api.subreddit(SUBREDDIT_NAME).new(limit=POST_LIMIT)
    
    # Filter out only those posts that we have not already fetched
    last_posts_filtered = [
        { 
            'title' : post.title, 
            'score' : post.score, 
            'selftext' : post.selftext, 
            'created' : post.created 
        } for post in last_posts if datetime.utcfromtimestamp(post.created) > last_update ]

    print(len(last_posts_filtered))

    # Add those posts to the DB
    if len(last_posts_filtered) > 0:
        db_client.create_many('posts', last_posts_filtered)

    print(f'Done fetching. Number of new posts: {len(last_posts_filtered)}')
