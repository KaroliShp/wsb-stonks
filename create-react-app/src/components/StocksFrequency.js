import React, { useState, useEffect }  from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Title from './Title';

/*
function preventDefault(event) {
  event.preventDefault();
}
*/

const useStyles = makeStyles(theme => ({
  seeMore: {
    marginTop: theme.spacing(3),
  },
}));

export default function StocksFrequency() {
  const classes = useStyles();

  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    fetch('/stock/frequency').then(res => res.json()).then(data => {
      setStocks(data);
    });
  }, []);

  return (
    <React.Fragment>
      <Title>Most Popular Stocks</Title>
      <Table size="big">
        <TableHead>
          <TableRow>
            <TableCell>Symbol</TableCell>
            <TableCell>Security</TableCell>
            <TableCell>Mentions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {stocks.map(stock => (
            <TableRow key={stock.id}>
              <TableCell>{stock.symbol}</TableCell>
              <TableCell>{stock.security}</TableCell>
              <TableCell>{stock.mentions}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </React.Fragment>
  );
}