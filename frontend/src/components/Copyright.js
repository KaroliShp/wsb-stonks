import React from 'react';
import Typography from '@material-ui/core/Typography';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';


export default function Copyright() {
    return (
      <Grid container spacing={0} justify='center'>
        <Grid item xs={12}>
          <Typography variant="body2" color="textSecondary" align="center">
            <b> Disclaimer & Terms of Use: </b>
          </Typography>
          <Typography paragraph="true" variant="body2" color="textSecondary" align="center">
            Our website is for informational purposes only. Nothing contained on our Site constitutes investment advice, solicitation, recommendation or endorsement of any investment strategies, practices, or individual decisions.
            By using this website, you have agreed to assume sole responsibility over assessing risks and merits associated with the use of any content found on the Site. Furthermore, you agree not to hold Site's creators liable for any claim for damages arising from any decision based on content on this Site.
          </Typography>
          <Typography variant="body2" color="textSecondary" align="center"> 
          <b> Statement on data sources: </b>
          </Typography>
          <Typography paragraph="true" variant="body2" color="textSecondary" align="center">  
            Data used for visualizations on this Site has been accessed over Reddit API from r/WallStreetBets subreddit.
          </Typography>
          <Typography variant="body2" color="textSecondary" align="center">
            <b> Contact information: </b> 
          </Typography>
          <Typography paragraph="true" variant="body2" color="textSecondary" align="center"> If you have any inquiries or questions, please contact    { ' ' }
            <Link color="inherit" href="mailto:karolis@spukas.com">
              <b>karolis@spukas.com</b>
            </Link><br/>
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="body2" color="textSecondary" align="center">
            {'Copyright © '}
            {new Date().getFullYear()}
          </Typography>
        </Grid>
      </Grid>
    );
  }