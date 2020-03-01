import React, { useState, useEffect }  from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Title from './Title';

export default function StocksFrequency() {
  const [keywords, setKeywords] = useState([]);

  useEffect(() => {
    fetch('/keyword/top').then(res => res.json()).then(data => {
      setKeywords(data);
    });
  }, []);

  return (
    <React.Fragment>
      <Title>Currently Trending</Title>
      <Table size="big">
        <TableHead>
          <TableRow>
            <TableCell>Keywords</TableCell>
            <TableCell>Mentions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {keywords.map(keyword => (
            <TableRow key={keyword.id}>
              <TableCell>{keyword.keyword}</TableCell>
              <TableCell>{keyword.mentions}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </React.Fragment>
  );
}