import React, { useState, useEffect }  from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Title from './Title';

export default function StocksFrequency() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    fetch('/api/stock/frequency/top').then(res => res.json()).then(data => {
      setStocks(data);
    });
  }, []);

  return (
    <React.Fragment>
      <Title>Most Popular Stonks</Title>
      <Table size="big">
        <TableHead>
          <TableRow>
            <TableCell>Symbol</TableCell>
            <TableCell>Post Mentions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {stocks.map(stock => (
            <TableRow key={stock.id}>
              <TableCell>{stock.stock_name}</TableCell>
              <TableCell>{stock.mentions}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </React.Fragment>
  );
}