import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import SvgIcon from '@material-ui/core/SvgIcon';
import logo from '../logo.png';


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
        <Toolbar>
            <img src={logo} className={classes.app_logo} alt="logo" />                
            <Typography variant="h6" className={classes.title}>
            r/WSB Stonks  💵💵💵
            </Typography>
        </Toolbar>
        </AppBar>
    </div>
  );
}