import React from 'react';
import CustomAppBar from './components/CustomAppBar';
import Copyright from './components/Copyright';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import StocksFrequency from './components/StocksFrequency';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({
  root: {
    
  },
  grid: {
    margin: 'auto',
  },
  paper: {
    padding: theme.spacing(2),
    display: 'flex',
    overflow: 'auto',
    flexDirection: 'column',
  },
}));

export default function App() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <CssBaseline />
      <CustomAppBar />
      <Grid className={classes.grid} item xs={12}>
        <Paper className={classes.paper}>
          <StocksFrequency />
        </Paper>
      </Grid>
      <Copyright />
    </div>
  );
}
