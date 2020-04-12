import React, { useState, useEffect }  from 'react';
import { useTheme } from '@material-ui/core/styles';
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer, CartesianGrid, Tooltip } from 'recharts';
import AutocompleteSearch from './AutocompleteSearch';
import Title from './Title';
import Spinner from './Spinner';
import { makeStyles } from '@material-ui/core/styles';


// Generate default data
function createData(time, amount) {
  return { time, amount };
}


const useStyles = makeStyles(theme => ({
  spinner: {
      textAlign: 'center',
      fontSize: "2.2em",
      margin: 'auto'
  },
}));


export default function StocksChart() {
  const theme = useTheme();

  const [chartData, setChartData] = useState([createData('00:00', 0)]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:5000/api/stock/frequency/historic/spy').then(res => res.json()).then(data => {
      setChartData(data);
      setLoading(false);
    });
  }, []);

  const onTagsChange = (event, values) => {
    if (values != null) {
      fetch('http://localhost:5000/api/stock/frequency/historic/' + values['stock_name'].toLowerCase()).then(res => res.json()).then(data => {
        setChartData(data);
      });
    }
  }

  const classes = useStyles();
  
  return (
    <React.Fragment>
      <Title>Stock Mentions in the Past 24 Hours</Title>
      <AutocompleteSearch onTagsChange={onTagsChange} />
      { 
      loading
      ?
      <div className={classes.spinner}>
        <Spinner />
      </div>
      :
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
          <Line type="linear" dataKey="amount" name="Mentions" stroke="#8884d8" activeDot={{r: 8}}/>
        </LineChart>
      </ResponsiveContainer>
      }
    </React.Fragment>
  );
}