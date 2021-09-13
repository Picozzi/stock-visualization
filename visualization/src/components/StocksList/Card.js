import React, { useState } from "react";
import styled from "styled-components";
import { motion, AnimatePresence } from "framer-motion";
import InitialCardContent from "./InitialCardContent";
import ExpandedCardContent from "./ExpandedCardContent";
import { useMediaQuery } from "react-responsive";
import "../../App.css";

const Base = styled(motion.div)`
  z-index: 2;
  position: relative;
  display: flex;
  height: 100%;
`;

const Cards = styled(motion.div)`
  font-family: Montserrat;
  padding-bottom: 50px;
`;

const Card = (props) => {
  const [isExpanded, setIsExpanded] = useState();
  const cardVariants = {
    inactive: {
      height: "15vh",
      width: "60vw",
      transition: {
        duration: 0.5,
        delay: 0.4,
      },
    },
    active: {
      height: "40vh",
      width: "60vw",
      transition: {
        duration: 0.5,
        delay: 0.6,
      },
    },
  };

  return (
    <Cards>
      <motion.div
        className={`card ${isExpanded ? "expanded" : "initial"}`}
        variants={cardVariants}
        animate={isExpanded ? "active" : "inactive"}
        inital="inactive"
      >
        <Base>
          <AnimatePresence initial={false} exitBeforeEnter>
            {!isExpanded ? (
              <InitialCardContent
                data={props.stock}
                onClick={setIsExpanded}
                key="initalContent"
              />
            ) : (
              <ExpandedCardContent
                data={props.stock}
                onClick={setIsExpanded}
                ket="expandedContent"
              />
            )}
          </AnimatePresence>
        </Base>
      </motion.div>
    </Cards>
  );
};

export default Card;
