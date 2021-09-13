import React from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
import { cardContentVariants, contentVariants } from "./variants";
import "../../App.css";
import { Icon } from "semantic-ui-react";
import "semantic-ui-css/semantic.min.css";
const CardBase = styled(motion.div)`
  background: white;
  width: 100%;
  height: 100%;
  border-radius: 15px;
`;

const Image = styled(motion.img)`
  max-width: 11vh;
  vertical-align: middle;
  border-radius: 15px;
  height: auto;
`;

const InitalCardContent = styled(motion.div)`
  height: 100%;
  padding-left: 2em;
  padding-right: 2em;
  display: flex;
  justify-content: space-between;
  align-items: center;
  a {
    text-decoration: none;
    color: #555555;
    font-weight: 500;
    font-size: 1em;
    cursor: pointer;
  }
`;

const Rank = styled.div`
  color: #555555;
  font-size: 3em;
  font-weight: 700;
`;
const Ticker = styled.div`
  color: #555555;
  font-size: 1.5vw;
  font-weight: 700;
`;

const Frequency = styled.div`
  color: ${(props) => props.color};
  display: flex;
  align-items: center;
`;

const FrequencyValue = styled.div`
  color: ${(props) => props.color};
  font-size: 1.6em;
  font-weight: 300;
  padding-right: 10px;
`;

const ProbabilityValue = styled.div`
  color: #555555;
  font-size: 1.2em;
  font-weight: 300;
`;
const InitalCard = ({ data, onClick }) => (
  <CardBase
    variants={cardContentVariants}
    exit="inactive"
    animate="active"
    initial="inactive"
  >
    <InitalCardContent variants={contentVariants}>
      <Rank>{data.rank}</Rank>

      <Image
        src={"https://eodhistoricaldata.com/img/logos/US/##.png".replace(
          "##",
          data.symbol
        )}
      />
      <Ticker>{data.symbol}</Ticker>
      <Frequency color="#679436">
        <FrequencyValue color="#98c765">
          {data.positive_frequency}
        </FrequencyValue>
        <Icon name="angle up" size="big" />
      </Frequency>
      <Frequency color="#D62839">
        <FrequencyValue color="#e05966">
          {data.negative_frequency}
        </FrequencyValue>
        <Icon name="angle down" size="big" />
      </Frequency>
      <ProbabilityValue>
        {Math.floor(data.probability * 100) + "% Certainty"}
      </ProbabilityValue>
      <a onClick={() => onClick(true)}>Chart</a>
    </InitalCardContent>
  </CardBase>
);

export default InitalCard;
