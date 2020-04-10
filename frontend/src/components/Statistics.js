import React, { useState, useEffect }  from 'react';
import Typography from '@material-ui/core/Typography';
import Link from '@material-ui/core/Link';

export default function Statistics() {

    const [statistics, setStatistics] = useState({ 
        'last_update' : 'LOADING',
        'total_posts' : 'LOADING',
        'total_comments' : 'LOADING',
        'top_author' : { 'user_name' : 'LOADING', 'posts' : 'LOADING' },
        'top_comments_author' : { 'user_name' : 'LOADING', 'posts' : 'LOADING' },
    });

    useEffect(() => {
        fetch('/api/statistics').then(res => res.json()).then(data => {
            setStatistics(data);
        });
    }, []);

    return (
        <div>
            <Typography variant="h6" align="center">
                Past 24 hours:
            </Typography>
            <Typography variant="subtitle1" align="center">
                💬 Number of posts analysed: <b>{ statistics.total_posts }</b>
            </Typography>
            <Typography variant="subtitle1" align="center">
                💬 Number of comments analysed: <b>{ statistics.total_comments }</b>
            </Typography>
            <Typography variant="subtitle1" align="center">
                🏆 <b>{ statistics.top_author.user_name }</b> is the most active poster with <b>{ statistics.top_author.posts }</b> posts
            </Typography>
            <Typography variant="subtitle1" align="center">
                🏆 <b>{ statistics.top_comments_author.user_name }</b> is the most active commenter with <b>{ statistics.top_comments_author.comments }</b> comments
            </Typography>
            <Typography variant="subtitle1" align="center">
                ⏰ Last update: <b>{ statistics.last_update }</b>
            </Typography>
        </div>
    );
  }