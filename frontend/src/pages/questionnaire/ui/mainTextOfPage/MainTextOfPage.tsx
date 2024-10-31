import React from 'react';
import styles from "./MainTextOfPage.module.scss";

interface HeaderTextProps {
  text: string;
}

const HeaderText: React.FC<HeaderTextProps> = ({ text }) => {
  return <h2 className={styles.mainTextOfTest}>{text}</h2>
};

export default HeaderText;
