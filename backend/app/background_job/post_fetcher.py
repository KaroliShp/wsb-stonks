from datetime import datetime, timedelta
import math

import praw
import json


class RedditPostFetcher:
    def __init__(self, client_id, client_secret, user_agent):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.USER_AGENT = user_agent
        self.SUBREDDIT_NAME = 'wallstreetbets'
    
    def fetch_posts(self, db_client, start_date, end_date, limit):
        """ 
        Fetch the newest raw posts from subreddit
        :param db_client:
        """

        #print(f'Start fetching, current update: {start_date.strftime("%Y-%m-%d %H:%M:%S")}; last update: {end_date.strftime("%Y-%m-%d %H:%M:%S")}')

        # Authenticate with reddit API
        reddit_api = praw.Reddit(client_id=self.CLIENT_ID,
                                client_secret=self.CLIENT_SECRET,
                                user_agent=self.USER_AGENT)

        # Get new posts that may contain duplicate posts from previous updates
        last_posts = reddit_api.subreddit(self.SUBREDDIT_NAME).new(limit=limit)

        # Proceed with only those posts that were created after the last update and are not in the system
        new_posts = []
        for post in last_posts:
            if datetime.utcfromtimestamp(post.created_utc) > end_date and datetime.utcfromtimestamp(post.created_utc) < start_date:
                # Append the new post information
                try:
                    new_posts.append({ 
                        'title' : post.title, 
                        'score' : post.score, 
                        'selftext' : post.selftext, 
                        'created' : datetime.utcfromtimestamp(post.created_utc).replace(microsecond=0),
                        'author' : post.author.name,
                        'url' : post.url,
                        'time_slot' : (start_date, end_date)
                    })
                except Exception:
                    # User/post deleted
                    pass

        """
        with open('posts.txt', 'w') as file:
            file.write(json.dumps(new_posts[:10], indent=4, sort_keys=True, default=str))
        """

        print(f'Done fetching. Number of new posts: {len(new_posts)}')

        return new_posts


    def fetch_comments(self, db_client, start_date, end_date, limit):
        """ 
        Fetch the newest raw posts from subreddit
        :param db_client:
        """

        # Authenticate with reddit API
        reddit_api = praw.Reddit(client_id=self.CLIENT_ID,
                                client_secret=self.CLIENT_SECRET,
                                user_agent=self.USER_AGENT)

        # Get new posts that may contain duplicate posts from previous updates
        last_comments = reddit_api.subreddit(self.SUBREDDIT_NAME).comments(limit=limit)

        # Proceed with only those posts that were created after the last update and are not in the system
        new_comments = []
        for comment in last_comments:
            if datetime.utcfromtimestamp(comment.created_utc) > end_date and datetime.utcfromtimestamp(comment.created_utc) < start_date :
                # Extract comments
                try:
                    new_comments.append({ 
                        'body' : comment.body, 
                        'author' : comment.author.name, 
                        'created' : datetime.utcfromtimestamp(comment.created_utc).replace(microsecond=0),
                        'url' : comment.permalink,
                        'time_slot' : (start_date, end_date)
                    })
                except Exception:
                    # User/comment deleted
                    pass

        """
        with open('comments.txt', 'w') as file:
            file.write(json.dumps(new_comments[:10], indent=4, sort_keys=True, default=str))
        """

        print(f'Done fetching. Number of new comments: {len(new_comments)}')

        return new_comments
