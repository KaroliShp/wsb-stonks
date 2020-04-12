import React, { useState, useEffect }  from 'react';
import { useTheme } from '@material-ui/core/styles';
import { LineChart, Line, XAxis, YAxis, Label, ResponsiveContainer, CartesianGrid, Tooltip, Text } from 'recharts';
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

  useEffect(() => {
    fetch('http://localhost:5000/api/stock/frequency/historic/spy').then(res => res.json()).then(data => {
      setChartData(data);
    });
}, []);

  const onTagsChange = (event, values) => {
    if (values != null) {
      fetch('http://localhost:5000/api/stock/frequency/historic/' + values['stock_name'].toLowerCase()).then(res => res.json()).then(data => {
        setChartData(data);
      });
    }
  }
  
  return (
    <React.Fragment>
      <AutocompleteSearch onTagsChange={onTagsChange} />
      <ResponsiveContainer>
        <LineChart
          data={chartData}
          margin={{
            top: 30,
            bottom: 50,
          }}
        >
          <Tooltip/>
          <CartesianGrid strokeDasharray="3 3"/>
          <XAxis interval={6} label={{ value: 'Past 24 hrs', position: 'insideBottom', offset: -10 }} dataKey="time" stroke={theme.palette.text.secondary} />
          <YAxis label={{ value: 'Mentions', angle: -90, position: 'insideLeft' }} allowDecimals="false" stroke={theme.palette.text.secondary} />
          <Line type="linear" dataKey="amount" name="mentions" stroke="#8884d8" activeDot={{r: 8}}/>
        </LineChart>
      </ResponsiveContainer>
    </React.Fragment>
  );
}