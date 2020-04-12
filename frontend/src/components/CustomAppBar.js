import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import logo from '../logo.png';
import EmojiText from './EmojiText';


const useStyles = makeStyles(theme => ({
  root: {
      flexGrow: 1,
  },
  title: {
      flexGrow: 1,
  },
  menuButton: {
      marginRight: theme.spacing(2),
  },
  app_logo: { 
      marginRight: theme.spacing(2), 
      height: 40,
      backgroundColor: 'white',
      borderRadius: 25,
  }
}));


export default function ButtonAppBar() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
        <AppBar position="static" style={{ background: 'black' }}>
        <Toolbar style={{ margin: 'auto' }}>
            <img src={logo} className={classes.app_logo} alt="logo" />                
            <Typography variant="h6" className={classes.title}>
            r/WSB Stonks  <EmojiText symbol="💵💵💵"/>
            </Typography>
        </Toolbar>
        </AppBar>
    </div>
  );
}