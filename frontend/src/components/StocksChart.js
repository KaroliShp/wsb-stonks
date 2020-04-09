import React, { useState, useEffect }  from 'react';
import { useTheme } from '@material-ui/core/styles';
import { LineChart, Line, XAxis, YAxis, Label, ResponsiveContainer } from 'recharts';
import Title from './Title';
import AutocompleteSearch from './AutocompleteSearch';

// Generate Sales Data
function createData(time, amount) {
  return { time, amount };
}

/*
const old_data = [
  createData('00:00', 0),
  createData('03:00', 300),
  createData('06:00', 600),
  createData('09:00', 800),
  createData('12:00', 1500),
  createData('15:00', 2000),
  createData('18:00', 2400),
  createData('21:00', 2400),
  createData('24:00', undefined),
];
*/

export default function StocksChart() {
  const theme = useTheme();

  const [chartData, setChartData] = useState([createData('00:00', 0)]);

  const onTagsChange = (event, values) => {
    if (values !== null) {
      fetch('/api/stock/frequency/historic/' + values['title'].toLowerCase()).then(res => res.json()).then(data => {
        setChartData(data);
      });
    }
    else {
      setChartData([createData('00:00', 0)])
    }
  }

  return (
    <React.Fragment>
      <Title>
          Time vs. Mentions of Stock
      </Title>
      <AutocompleteSearch onTagsChange={onTagsChange} />
      <ResponsiveContainer>
        <LineChart
          data={chartData}
          margin={{
            top: 30,
            right: 30,
            bottom: 50,
            left: 30,
          }}
        >
          <XAxis dataKey="time" stroke={theme.palette.text.secondary} />
          <YAxis stroke={theme.palette.text.secondary} />
          <Line type="monotone" dataKey="amount" stroke={theme.palette.primary.dark} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </React.Fragment>
  );
}