/* eslint-disable no-use-before-define */
import React, { useState, useEffect }  from 'react';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';

export default function AutocompleteSearch(props) {
  
  const [stocks, setStocks] = useState([{ 'stock_name' : 'SPY' }]);

  useEffect(() => {
    fetch('https://wsbstonks.com/api/stock/list').then(res => res.json()).then(data => {
      setStocks(data);
    });
  }, []);
  
  const options = stocks.map(option => {
    const firstLetter = option.stock_name[0].toUpperCase();
    return {
      firstLetter: /[0-9]/.test(firstLetter) ? '0-9' : firstLetter,
      ...option,
    };
  });

  return (
    <Autocomplete
      id="grouped-demo"
      options={options.sort((a, b) => -b.firstLetter.localeCompare(a.firstLetter))}
      groupBy={option => option.firstLetter}
      getOptionLabel={option => option.stock_name}
      style={{ width: 300, marginTop: '20px' }}
      onChange={props.onTagsChange}
      defaultValue={{'stock_name' : 'SPY'}}
      renderInput={params => <TextField {...params} label="Enter stock symbol" variant="outlined" />}
    />
  );
}