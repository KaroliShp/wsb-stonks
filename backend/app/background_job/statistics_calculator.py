def calculate_statistics(db_client, new_posts_by_date, update_date):
    total_posts = 0
    total_comments = 0
    authors = {}

    # Get available info from the posts
    for date, new_posts in new_posts_by_date.items():
        # Get number of posts
        total_posts += len(new_posts)
        for post in new_posts:
            # Get number of comments
            total_comments += post['num_comments']
            # Get authors
            if post['author'] in authors:
                authors[post['author']] += 1
            else:
                authors[post['author']] = 1
    
    # Append statistics to a DB object
    statistics = { 'last_update' : update_date }
    statistics['total_posts'] = total_posts
    statistics['total_comments'] = total_comments
    top_author = sorted([ (author, posts) for author, posts in authors.items() ], key=lambda x: x[1], reverse=True)[0]
    statistics['top_author'] = { 'user_name' : top_author[0], 'posts' : top_author[1]  } 

    # Write to DB
    db_client.delete_many('statistics', {})
    db_client.create('statistics', statistics)