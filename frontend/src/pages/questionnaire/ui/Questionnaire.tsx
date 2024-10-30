import { useState } from "react";
import styles from "./Questionnaire.module.scss";
import { Header } from "../../../widgets/header";
import CircleToggle from "./circleToggle/CircleToggle";
import { data } from "../api/getRequestion";
import {useNavigate} from "react-router-dom"
import prevButtonSvg from "../../../assets/prevButton.svg";
import HeaderText from "./mainTextOfPage/MainTextOfPage";

export const Questionnaire = () => {
	const navigate = useNavigate();

  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const totalQuestions = data.total_questions;
  const [answers, setAnswers] = useState<string[]>(Array(totalQuestions).fill(''));

  const handleNextQuestion = () => {
    if (currentQuestionIndex < totalQuestions - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      navigate("/answer_test");
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleAnswerSelect = (text: string) => {
    const newAnswers = [...answers];
    newAnswers[currentQuestionIndex] = newAnswers[currentQuestionIndex] === text ? '' : text;
    setAnswers(newAnswers);
  };

  return (
    <>
      <Header />
      <div>
				<HeaderText text={"Выберите утверждение, которое вам ближе"} />
      </div>

      <div className={styles.divForCountOfQuestion}>
        <p>
          {currentQuestionIndex + 1}/{totalQuestions}
        </p>
      </div>
      <hr className={styles.hr} />

      <div className={styles.divForAnswer}>
        {Object.values(data.questions[currentQuestionIndex]).map((text, index) => (
          <CircleToggle
            key={index}
            text={text}
            isFilled={answers[currentQuestionIndex] === text}
            onSelect={handleAnswerSelect}
          />
        ))}
      </div>

      <div className={styles.buttonContainer}>
        {currentQuestionIndex > 0 && (
          <button className={styles.prevButton} onClick={handlePreviousQuestion}>
            <img src={prevButtonSvg} alt="" />
          </button>
        )}
        <button className={currentQuestionIndex === 0 ? styles.nextButton : styles.nextButtonSolo} onClick={handleNextQuestion}>
          Далее
        </button>
      </div>
    </>
  );
};

export default Questionnaire;
