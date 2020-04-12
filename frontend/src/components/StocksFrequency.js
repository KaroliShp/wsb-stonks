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


export default function StocksFrequency() {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://wsbstonks.com/api/stock/frequency/top').then(res => res.json()).then(data => {
      setStocks(data);
      setLoading(false);
    });
  }, []);

  const classes = useStyles();

  return (
    <React.Fragment>
      <Title>Most Popular Stonks</Title>
      { loading 
        ?
        <div className={classes.spinner}>
          <Spinner />
        </div>
        :
        <Table size="big">
          <TableHead>
            <TableRow>
              <TableCell align='center'>Symbol</TableCell>
              <TableCell align='center'>Mentions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {stocks.map(stock => (
              <TableRow key={stock.id}>
                <TableCell align='center'>{stock.stock_name}</TableCell>
                <TableCell align='center'>{stock.mentions}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        }
    </React.Fragment>
  );
}