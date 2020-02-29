import praw

from nlp_engine.io import write_to_file


CLIENT_ID = '2ocFsBoC1x3Ikw'
CLIENT_SECRET = 'j2CbxQJb53NFdqANAM60p1xCbt4'
REDIRECT_URI = 'http://localhost:8080'
USER_AGENT = 'wsb-stonks'


def authenticate():
    return praw.Reddit(client_id=CLIENT_ID,
                       client_secret=CLIENT_SECRET,
                       user_agent=USER_AGENT)


def get_posts_today(reddit):
    return reddit.subreddit('wallstreetbets').new(limit=100)


def main():
    reddit = authenticate()
    data = get_posts_today(reddit)
    write_to_file(data)


if __name__ == '__main__':
    main()
