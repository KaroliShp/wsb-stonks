def calculate_statistics(db_client, new_entries_by_date, update_date):
    print('Start calculating statistics')

    # Statistics to track
    total_posts = 0
    total_comments = 0
    post_authors = {}
    comment_authors = {}
    posts_activity = []
    comments_activity = []

    # Get info from posts and comments
    for date, new_entries in new_entries_by_date.items():
        # Get number of posts for the date
        total_posts += len(new_entries['posts'])
        posts_activity.append({ 'time' : date.strftime("%H:%M"), 'amount' : len(new_entries['posts']) })
        for post in new_entries['posts']:
            # Get post authors
            if post['author'] in post_authors:
                post_authors[post['author']] += 1
            else:
                post_authors[post['author']] = 1
        
        # Get number of comments for the date
        total_comments += len(new_entries['comments'])
        comments_activity.append({ 'time' : date.strftime("%H:%M"), 'amount' : len(new_entries['comments']) })
        for comment in new_entries['comments']:
            # Get comment authors
            if comment['author'] in comment_authors:
                comment_authors[comment['author']] += 1
            else:
                comment_authors[comment['author']] = 1
        
    # Append statistics to a DB object
    statistics = { 'last_update' : update_date }
    statistics['total_posts'] = total_posts
    statistics['total_comments'] = total_comments
    top_post_author = sorted([ (author, posts) for author, posts in post_authors.items() ], key=lambda x: x[1], reverse=True)[0]
    statistics['top_post_author'] = { 'user_name' : top_post_author[0], 'posts' : top_post_author[1]  } 
    top_comments_author = sorted([ (author, comments) for author, comments in comment_authors.items() ], key=lambda x: x[1], reverse=True)[0]
    statistics['top_comments_author'] = { 'user_name' : top_comments_author[0], 'comments' : top_comments_author[1]  } 
    statistics['posts_activity'] = posts_activity
    statistics['comments_activity'] = comments_activity

    print('End calculating statistics')

    return statistics