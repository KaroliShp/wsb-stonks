import React, { useState, useEffect }  from 'react';
import { useTheme } from '@material-ui/core/styles';
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer, CartesianGrid, Tooltip } from 'recharts';
import Title from './Title';

// Generate default data
function createData(time, amount) {
  return { time, amount };
}


export default function CommentActivityChart() {
  const theme = useTheme();

  const [chartData, setChartData] = useState([createData('00:00', 0)]);

  useEffect(() => {
    fetch('http://localhost:5000/api/statistics/activity/comments').then(res => res.json()).then(data => {
      setChartData(data);
    });
}, []);
  
  return (
    <React.Fragment>
        <Title>Comment Activity</Title>
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
          <YAxis label={{ value: 'New Comments', angle: -90, position: 'insideLeft' }} allowDecimals="false" stroke={theme.palette.text.secondary} />
          <Line type="linear" dataKey="amount" name="Comments" stroke="#8884d8" activeDot={{r: 8}}/>
        </LineChart>
      </ResponsiveContainer>
    </React.Fragment>
  );
}