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


export default function Keywords() {
  const [keywords, setKeywords] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/keyword/top').then(res => res.json()).then(data => {
      setKeywords(data);
      setLoading(false);
    });
  }, []);

  const classes = useStyles();

  return (
    <React.Fragment>
      <Title>Currently Trending</Title>
      { loading 
        ?
        <div className={classes.spinner}>
          <Spinner />
        </div>
        :
        <Table size="big">
          <TableHead>
            <TableRow>
              <TableCell align='center'>Keywords</TableCell>
              <TableCell align='center'>Mentions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {keywords.map(keyword => (
              <TableRow key={keyword.id}>
                <TableCell align='center'>{keyword.keyword}</TableCell>
                <TableCell align='center'>{keyword.mentions}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      }
    </React.Fragment>
  );
}