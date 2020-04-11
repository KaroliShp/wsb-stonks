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
    # Calculate the last update date based on how many number of updates (each 1 hr long) we need to perform
    last_update = update_date - timedelta(hours=num_of_updates)

    print(f'Start fetching, current update: {update_date.strftime("%Y-%m-%d %H:%M:%S")}; last update: {last_update.strftime("%Y-%m-%d %H:%M:%S")}')

    # Authenticate with reddit API
    reddit_api = praw.Reddit(client_id=CLIENT_ID,
                             client_secret=CLIENT_SECRET,
                             user_agent=USER_AGENT)

    # Get new posts that may contain duplicate posts from previous updates
    last_posts = reddit_api.subreddit(SUBREDDIT_NAME).new(limit=limit)

    # Proceed with only those posts that were created after the last update and are not in the system
    new_posts = []
    new_comments = []
    for post in last_posts:
        if datetime.utcfromtimestamp(post.created_utc) > last_update:
            # Append the new post information
            try:
                new_posts.append({ 
                    'title' : post.title, 
                    'score' : post.score, 
                    'selftext' : post.selftext, 
                    'created' : datetime.utcfromtimestamp(post.created_utc).replace(microsecond=0),
                    'author' : post.author.name,
                    'num_comments' : post.num_comments,
                    'url' : post.url
                })
            except Exception:
                # User/post deleted
                pass
            
            # Flatten responses to comments (MoreComments)
            post.comments.replace_more(limit=0)
            # Extract its comments (they are at least as old as the post)
            for comment in post.comments.list():
                try:
                    new_comments.append({ 
                        'body' : comment.body, 
                        'author' : comment.author.name, 
                        'created' : datetime.utcfromtimestamp(comment.created_utc).replace(microsecond=0),
                        'url' : comment.permalink
                    })
                except Exception:
                    # User/comment deleted
                    pass

    # New entries include both comments and posts for a specific time interval (in this case hourly update)
    new_entries_by_date = {}
    for i in range(0, num_of_updates):
        new_entries_by_date[update_date - timedelta(hours=i)] = { 'posts' : [], 'comments' : [] }

    # Group posts into date hourly based on their creation date
    for post in new_posts:
        update_diff = math.floor(((update_date - post['created']).total_seconds() / 3600))
        new_entries_by_date[update_date - timedelta(hours=update_diff)]['posts'].append(post)

    # Group comments into hourly intervals based on their creation date
    for comment in new_comments:
        update_diff = math.floor(((update_date - comment['created']).total_seconds() / 3600))
        try:
            new_entries_by_date[update_date - timedelta(hours=update_diff)]['comments'].append(comment)
        except Exception:
            # Some comments are fetched after the update date is fixed, so it appears as if its from the future
            pass

    print(f'Done fetching. Number of new posts: {len(new_posts)}. Number of new comments: {len(new_comments)}')

    return new_entries_by_date
