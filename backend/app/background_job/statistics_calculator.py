def calculate_statistics(db_client, new_posts, new_comments, start_date, end_date):
    print('Start calculating statistics')
    
    # Statistics to track
    total_posts = len(new_posts)
    total_comments = len(new_comments)
    post_authors = {}
    comment_authors = {}
    posts_activity = []
    comments_activity = []

    # Update all post authors
    for post in new_posts:
        if post['author'] in post_authors:
            post_authors[post['author']] += 1
        else:
            post_authors[post['author']] = 1

    # Update all commentators
    for comment in new_comments:
        if comment['author'] in comment_authors:
            comment_authors[comment['author']] += 1
        else:
            comment_authors[comment['author']] = 1

    # Append statistics to a DB object
    statistics = { 'start_date' : start_date }
    statistics['end_date'] = end_date
    statistics['total_posts'] = total_posts
    statistics['total_comments'] = total_comments
    statistics['top_post_authors'] = post_authors
    statistics['top_comments_author'] = comment_authors

    print('End calculating statistics')

    return statistics