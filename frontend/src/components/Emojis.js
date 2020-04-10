import React, { useState, useEffect }  from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Title from './Title';

export default function Emojis() {
  const [emojis, setEmojis] = useState([]);

  useEffect(() => {
    fetch('/api/emoji/top').then(res => res.json()).then(data => {
      setEmojis(data);
    });
  }, []);

  return (
    <React.Fragment>
      <Title>Currently Trending</Title>
      <Table size="big">
        <TableHead>
          <TableRow>
            <TableCell>Emoji</TableCell>
            <TableCell>Mentions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {emojis.map(emoji => (
            <TableRow key={emoji.id}>
              <TableCell>{emoji.emoji}</TableCell>
              <TableCell>{emoji.mentions}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </React.Fragment>
  );
}