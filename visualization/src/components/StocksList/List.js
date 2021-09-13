import React, { useState, useEffect } from "react";
import "../../App.css";
import styled from "styled-components";
import Card from "./Card";
import axios from "axios";
import LoadingAnimation from "./load.gif";

const Section = styled.section`
  display: flex;
  background-color: #f5f5f5;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  h1 {
    margin-bottom: 0.5rem;
    font-family: Montserrat;
    color: #555555;
    font-size: 3vw;
    padding-top: 40px;
    padding-bottom: 2em;
  }
`;

const LoadingDiv = styled.div`
  height: 100vh;
  width: 100vw;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const LoadingSpan = styled.span`
  display: inline-block;
`;

const LoadingImg = styled.img`
  width: 50%;
`;

const LoadingScreen = () => {
  return (
    <LoadingDiv>
      <LoadingSpan>
        <LoadingImg src={LoadingAnimation} />
      </LoadingSpan>
    </LoadingDiv>
  );
};

const List = () => {
  const [stockList, setStockList] = useState(null);
  const api_url = "http://localhost:5000/aggregation";
  useEffect(() => {
    axios
      .get(api_url)
      .then((response) => {
        console.log("SUCCESS", response);
        setStockList(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <div>
      {stockList == null ? <LoadingScreen /> : <StockView data={stockList} />}
    </div>
  );
};

const StockView = (props) => {
  const list = props.data;
  return (
    <Section id={props.id}>
      <h1>Top 10 Mentioned Social Media Stocks</h1>
      {list.map((item, key) => (
        <Card stock={item} id={key} />
      ))}
    </Section>
  );
};

export default List;
