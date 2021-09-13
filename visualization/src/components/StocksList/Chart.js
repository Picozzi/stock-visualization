import React from "react";
import {
  LineChart,
  Line,
  Label,
  XAxis,
  YAxis,
  CartesianGrid,
  Legend,
} from "recharts";

const agvvgs = [
  {
    normalized_date: 1630886400000,
    sentiment: 0.34,
    "closing price": null,
  },
  {
    normalized_date: 1630972800000,
    sentiment: 0.43,
    "closing price ($)": 199.0,
  },
  {
    normalized_date: 1631059200000,
    sentiment: 0.42,
    "closing price ($)": 198.8000030518,
  },
  {
    normalized_date: 1631145600000,
    sentiment: 0.24,
    "closing price ($)": 199.1799926758,
  },
  {
    normalized_date: 1631232000000,
    sentiment: 0.34,
    "closing price ($)": 190.4100036621,
  },
  {
    normalized_date: 1631318400000,
    sentiment: 0.19,
    "closing price ($)": null,
  },
  {
    normalized_date: 1631404800000,
    sentiment: 0.31,
    "closing price ($)": null,
  },
];

const Chart = (props) => {
  function formatXAxis(tickItem) {
    var a = new Date(tickItem);
    var months = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = a.getUTCDate();
    return month + " " + date + " " + year;
  }

  function formatYAxis(tickItem) {
    return tickItem.toFixed(2);
  }
  return (
    <LineChart
      width={920}
      height={325}
      data={props.chart_data}
      margin={{
        top: 5,
        right: 20,
        left: 30,
        bottom: 5,
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis
        dataKey="normalized_date"
        domain={["dataMin", "dataMax"]}
        tickFormatter={formatXAxis}
      />
      <YAxis
        yAxisId="right"
        orientation="right"
        domain={[0, 1]}
        label={{
          value: "Sentiment (0 - Negative and 1 - Positive)",
          angle: -90,
          offset: -5,
          dy: 10,
          position: "insideTopRight",
        }}
      />
      <YAxis
        yAxisId="left"
        orientation="left"
        domain={["dataMin", "dataMax"]}
        tickFormatter={formatYAxis}
        label={{
          value: "Closing Price ($)",
          angle: -90,
          dy: 70,
          offset: -10,

          position: "insideLeft",
        }}
      />
      <Legend />
      <Line
        yAxisId="right"
        type="monotone"
        dataKey="sentiment"
        stroke="#82ca9d"
      />
      //{" "}
      <Line
        yAxisId="left"
        type="monotone"
        dataKey="closing price"
        stroke="#8884d8"
        activeDot={{ r: 8 }}
      />
    </LineChart>
  );
};
export default Chart;
