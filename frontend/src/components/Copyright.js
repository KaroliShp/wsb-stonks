import React from 'react';
import Typography from '@material-ui/core/Typography';
import Link from '@material-ui/core/Link';

export default function Copyright() {
    return (
      <Typography variant="body2" color="textSecondary" align="center">
        {'Copyright © '}
        <Link color="inherit" href="https://github.com/KaroliShp">
          Karolishp
        </Link>{' '}
        and &nbsp;
        <Link color="inherit" href="https://github.com/r-k-jonynas">
          r-k-jonynas
        </Link>{' '}
        {new Date().getFullYear()}
        {'.'}
      </Typography>
    );
  }