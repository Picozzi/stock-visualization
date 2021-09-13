import React from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
import { expandedVariants, contentBlockVariants } from "./variants";
import "../../App.css";
import { Icon } from "semantic-ui-react";
import Chart from "./Chart";

const CardBase = styled(motion.div)`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background: white;
  border-radius: 15px;
  width: 100%;
  height: 100%;
  @media (min-width: 1575px) {
    padding-left: 0;
  }
`;

const ExpandedCardContent = styled(motion.div)`
  padding-left: 1em;
  padding-top: 1.1em;
`;

const Close = styled(motion.div)`
  margin-top: 1vw;
  margin-right: 1vw;
  a {
    color: #555555;
    cursor: pointer;
    text-decoration: none;
  }
`;

const AnimatedContentBlock = ({ children }) => (
  <motion.div variants={contentBlockVariants}>{children}</motion.div>
);

const ExpandedCard = ({ data, onClick }) => {
  return (
    <CardBase
      variants={expandedVariants}
      animate="active"
      initial="inactive"
      exit="exit"
    >
      <ExpandedCardContent>
        <AnimatedContentBlock>
          <Chart chart_data={data.chart_data} />
        </AnimatedContentBlock>
      </ExpandedCardContent>

      <AnimatedContentBlock>
        <Close color="#555555">
          <a onClick={() => onClick(false)}>
            <Icon name="close" size="large" />
          </a>
        </Close>
      </AnimatedContentBlock>
    </CardBase>
  );
};

export default ExpandedCard;
