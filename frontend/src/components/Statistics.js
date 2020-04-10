import React, { useState, useEffect }  from 'react';
import Typography from '@material-ui/core/Typography';
import Link from '@material-ui/core/Link';

export default function Statistics() {

    const [statistics, setStatistics] = useState({ 
        'last_update' : 'NaN',
        'total_posts' : 'NaN',
        'total_comments' : 'NaN',
        'top_author' : { 'user_name' : 'NaN', 'posts' : 'NaN' }
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
            <Typography variant="h6" align="center">
                💬 Number of posts analysed: { statistics.total_posts }
            </Typography>
            <Typography variant="h6" align="center">
                💬 Number of comments analysed: { statistics.total_comments }
            </Typography>
            <Typography variant="h6" align="center">
                🏆 { statistics.top_author.user_name } is the most activate poster with { statistics.top_author.posts } posts
            </Typography>
            <Typography variant="h6" align="center">
                ⏰ Last update: { statistics.last_update }
            </Typography>
        </div>
    );
  }