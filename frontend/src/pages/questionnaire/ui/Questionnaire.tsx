import { useState } from "react";
import styles from "./Questionnaire.module.scss";
import { Header } from "../../../widgets/header";
import CircleToggle from "./circleToggle/CircleToggle";
import { data } from "../api/getRequestion";
import { useNavigate } from "react-router-dom";
import prevButtonSvg from "../../../assets/prevButton.svg";
import HeaderText from "./mainTextOfPage/MainTextOfPage";

export const Questionnaire = () => {
  const navigate = useNavigate();
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const totalQuestions = data.total_questions;

  const [answers, setAnswers] = useState<(number | null)[]>(
    Array(totalQuestions).fill(null)
  );

  const handleNextQuestion = () => {
    if (currentQuestionIndex < totalQuestions - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
			console.log(answers)
      navigate("/answer_test");
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleAnswerSelect = (index: number) => {
    const newAnswers = [...answers];
    newAnswers[currentQuestionIndex] =
      newAnswers[currentQuestionIndex] === index ? null : index;
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
            isFilled={answers[currentQuestionIndex] === index}
            onSelect={() => handleAnswerSelect(index)}
          />
        ))}
      </div>

      <div className={styles.buttonContainer}>
        {currentQuestionIndex > 0 && (
          <button className={styles.prevButton} onClick={handlePreviousQuestion}>
            <img src={prevButtonSvg} alt="" />
          </button>
        )}
        <button
          className={currentQuestionIndex === 0 ? styles.nextButton : styles.nextButtonSolo}
          onClick={handleNextQuestion}
        >
          Далее
        </button>
      </div>
    </>
  );
};

export default Questionnaire;
