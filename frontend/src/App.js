import React from 'react';
import clsx from 'clsx';
import CustomAppBar from './components/CustomAppBar';
import Copyright from './components/Copyright';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import StocksFrequency from './components/StocksFrequency';
import { makeStyles } from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';
import Container from '@material-ui/core/Container';
import Keywords from './components/Keywords';
import StocksChart from './components/StocksChart';
import AutocompleteSearch from './components/AutocompleteSearch';

const useStyles = makeStyles(theme => ({
  root: {
    
  },
  grid: {
    margin: 'auto',
  },
  appBarSpacer: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    height: '100vh',
    overflow: 'auto',
  },
  container: {
    paddingTop: theme.spacing(1),
    paddingBottom: theme.spacing(1),
  },
  paper: {
    padding: theme.spacing(2),
    display: 'flex',
    overflow: 'auto',
    flexDirection: 'column',
  },
  fixedHeight: {
    height: '50vh',
  },
}));

export default function App() {
  const classes = useStyles();
  const fixedHeightPaper = clsx(classes.paper, classes.fixedHeight);

  return (
    <div className={classes.root}>
      <CssBaseline />
      <CustomAppBar />
      <main className={classes.content}>
        <div className={classes.appBarSpacer} />
        <Container maxWidth="lg" className={classes.container}>

          <Grid container spacing={3}>

            <Grid item xs={12}>
              <AutocompleteSearch />
            </Grid>

            <Grid item xs={12}>
              <Paper className={fixedHeightPaper}>
                <StocksChart />
              </Paper>
            </Grid>

            <Grid item xs={12} md={6}>
              <Paper className={classes.paper}>
                <Keywords />
              </Paper>
            </Grid>

            <Grid className={classes.grid} item xs={12} md={6}>
              <Paper className={classes.paper}>
                <StocksFrequency />
              </Paper>
            </Grid>

          </Grid>

          <Box pt={4}>
            <Copyright />
          </Box>

        </Container>
      </main>
    </div>
  );
}