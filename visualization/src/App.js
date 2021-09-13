import React, { Component } from "react";
import List from "./components/StocksList/List";
import styled from "styled-components";

const AppHolder = styled.div`
  font-family: Montserrat;
`;

export default class App extends Component {
  render() {
    return (
      <AppHolder>
        <List title="List of Stocks" id="stock_list" />
      </AppHolder>
    );
  }
}
