import React, { useState, useEffect }  from 'react';
import Typography from '@material-ui/core/Typography';
import EmojiText from './EmojiText';


export default function Statistics() {

    const [statistics, setStatistics] = useState({ 
        'last_update' : 'LOADING',
        'total_posts' : 'LOADING',
        'total_comments' : 'LOADING',
        'top_poster' : { 'user_name' : 'LOADING', 'posts' : 'LOADING' },
        'top_commenter' : { 'user_name' : 'LOADING', 'posts' : 'LOADING' },
    });

    useEffect(() => {
        const isProduction = (process.env.NODE_ENV === 'production');
        const ipAddr = (isProduction ? 'https://wsbstonks.com/' : 'http://127.0.0.1:5000/');
        fetch(ipAddr.concat('api/statistics')).then(res => res.json()).then(data => {
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
                <EmojiText symbol="🏆"/> <b>{ statistics.top_poster.user_name }</b> is the most active poster with <b>{ statistics.top_poster.posts }</b> posts
            </Typography>
            <Typography variant="subtitle1" align="center">
                <EmojiText symbol="🏆"/> <b>{ statistics.top_commenter.user_name }</b> is the most active commenter with <b>{ statistics.top_commenter.comments }</b> comments
            </Typography>
            <Typography variant="subtitle1" align="center">
                <EmojiText symbol="⏰"/> Last update: <b>{ statistics.last_update }</b>
            </Typography>
        </div>
    );
  }