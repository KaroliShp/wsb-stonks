import React, { useState, useEffect }  from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Title from './Title';
import Spinner from './Spinner';
import { makeStyles } from '@material-ui/core/styles';


const useStyles = makeStyles(theme => ({
  spinner: {
      textAlign: 'center',
      fontSize: "2.2em",
      margin: 'auto'
  },
}));


export default function Emojis() {
  const [emojis, setEmojis] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:5000/api/emoji/top').then(res => res.json()).then(data => {
      setEmojis(data);
      setLoading(false);
    });
  }, []);

  const classes = useStyles();

  return (
    <React.Fragment>
      <Title>Top 🅱️emoji</Title>
      { loading
        ?
        <div className={classes.spinner}>
          <Spinner />
        </div>
        :
        <Table size="big">
        <TableHead>
          <TableRow>
            <TableCell align='center'>Emoji</TableCell>
            <TableCell align='center'>Mentions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {emojis.map(emoji => (
            <TableRow key={emoji.id}>
              <TableCell align='center'>{emoji.emoji}</TableCell>
              <TableCell align='center'>{emoji.mentions}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      }
    </React.Fragment>
  );
}