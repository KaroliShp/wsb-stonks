import React, { useState, useEffect }  from 'react';
import Typography from '@material-ui/core/Typography';
import EmojiText from './EmojiText';


export default function Statistics() {

    const [statistics, setStatistics] = useState({ 
        'last_update' : 'LOADING',
        'total_posts' : 'LOADING',
        'total_comments' : 'LOADING',
        'top_post_author' : { 'user_name' : 'LOADING', 'posts' : 'LOADING' },
        'top_comments_author' : { 'user_name' : 'LOADING', 'posts' : 'LOADING' },
    });

    useEffect(() => {
        fetch('https://wsbstonks.com/api/statistics').then(res => res.json()).then(data => {
            setStatistics(data);
        });
    }, []);

    return (
        <div>
            <Typography variant="h6" align="center">
                Past 24 Hours:
            </Typography>
            <Typography variant="subtitle1" align="center">
                <EmojiText symbol="💬"/> Number of posts analysed: <b>{ statistics.total_posts }</b>
            </Typography>
            <Typography variant="subtitle1" align="center">
                <EmojiText symbol="💬"/> Number of comments analysed: <b>{ statistics.total_comments }</b>
            </Typography>
            <Typography variant="subtitle1" align="center">
                <EmojiText symbol="🏆"/> <b>{ statistics.top_post_author.user_name }</b> is the most active poster with <b>{ statistics.top_post_author.posts }</b> posts
            </Typography>
            <Typography variant="subtitle1" align="center">
                <EmojiText symbol="🏆"/> <b>{ statistics.top_comments_author.user_name }</b> is the most active commenter with <b>{ statistics.top_comments_author.comments }</b> comments
            </Typography>
            <Typography variant="subtitle1" align="center">
                <EmojiText symbol="⏰"/> Last update: <b>{ statistics.last_update }</b>
            </Typography>
        </div>
    );
  }