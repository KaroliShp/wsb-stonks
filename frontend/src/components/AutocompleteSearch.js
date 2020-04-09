/* eslint-disable no-use-before-define */
import React, { useState, useEffect }  from 'react';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';

export default function AutocompleteSearch(props) {
  const options = all_stocks.map(option => {
    const firstLetter = option.title[0].toUpperCase();
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
      getOptionLabel={option => option.title}
      style={{ width: 300 }}
      onChange={props.onTagsChange}
      renderInput={params => <TextField {...params} label="Enter stock symbol" variant="outlined" />}
    />
  );
}

const all_stocks = [
  { title: 'SPY'},
];