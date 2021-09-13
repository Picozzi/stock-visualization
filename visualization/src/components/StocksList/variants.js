export const cardContentVariants = {
  inactive: {
    transition: {
      staggerChildren: 0.3,
      duration: 0.4,
      delay: 0.4,
    },
  },
  active: {
    transition: {
      staggerChildren: 0.3,
      delayChildren: 0.3,
      duration: 0.4,
      staggerDirection: -1,
      delay: 0.4,
    },
  },
};

export const contentVariants = {
  inactive: {
    x: 0,
    y: 0,
    opacity: 0,
    transition: {
      duration: 0.4,
    },
  },
  active: {
    x: 0,
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.4,
    },
  },
};

export const expandedVariants = {
  inactive: {
    opacity: 0,
  },
  active: {
    opacity: 1,
    transition: {
      staggerChildren: 0.3,
      delayChildren: 0.3,
    },
  },
};

export const contentBlockVariants = {
  inactive: {
    opacity: 0,
    y: 0,
  },
  active: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.5,
    },
  },
  exit: {
    opacity: 0,
    y: 0,
    transition: {
      duration: 0.4,
    },
  },
};
