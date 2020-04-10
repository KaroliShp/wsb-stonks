import React from 'react';
import Typography from '@material-ui/core/Typography';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';


export default function Copyright() {
    return (
      <Grid container spacing={0} justify='center'>
        <Grid item xs={12}>
          <Typography variant="body2" color="textSecondary" align="center">
            Ši svetainė nėra oficiali ir yra tik informacinio pobūdžio, autoriai neatsako už svetainės naudojimą. Duomenys surinkti iš viešai prieinamos informacijos internete (naujienų portalai bei SAM). Radę klaidų, praneškite { ' ' } 
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