import React from 'react';
import styles from './CircleToggle.module.scss';

const CircleToggle: React.FC<{ text: string; isFilled: boolean; onSelect: (text: string) => void; }> = ({ text, isFilled, onSelect }) => {
  const handleToggle = () => {
    onSelect(text);
  };

  return (
    <div className={`${styles.divForCircleToggle}`}>
      <div
        onClick={handleToggle}
        className={`${styles.circleToggle} ${isFilled ? styles.full : ''}`}
      />
      <p className={`${styles.answerText} ${isFilled ? styles.textFull : ''}`}>{text}</p>
    </div>
  );
};

export default CircleToggle;
