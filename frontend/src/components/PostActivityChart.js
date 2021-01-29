import React, { useState, useEffect }  from 'react';
import { useTheme } from '@material-ui/core/styles';
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer, CartesianGrid, Tooltip } from 'recharts';
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


export default function PostActivityChart() {
  const theme = useTheme();

  const [chartData, setChartData] = useState([createData('00:00', 0)]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/statistics/activity/posts').then(res => res.json()).then(data => {
      setChartData(data);
      setLoading(false);
    });
    }, []);

    const classes = useStyles();
  
  return (
    <React.Fragment>
        <Title>New Posts in the Past 24 Hours</Title>
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
                    bottom: 30,
                }}
                >
                <Tooltip/>
                <CartesianGrid strokeDasharray="3 3"/>
                <XAxis interval={6} label={{ value: 'Past 24 hrs', position: 'insideBottom', offset: -10 }} dataKey="time" stroke={theme.palette.text.secondary} />
                <YAxis label={{ value: 'New Posts', angle: -90, position: 'insideLeft' }} allowDecimals="false" stroke={theme.palette.text.secondary} />
                <Line type="linear" dataKey="amount" name="Posts" stroke="#8884d8" activeDot={{r: 8}}/>
                </LineChart>
            </ResponsiveContainer>
        }
    </React.Fragment>
  );
}