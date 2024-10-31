import { useState, useEffect } from "react";
import styles from "./Questionnaire.module.scss";
import { Header } from "../../../widgets/header";
import CircleToggle from "./circleToggle/CircleToggle";
import { fetchQuestions } from "../api/getRequestion";
import { useNavigate } from "react-router-dom";
import prevButtonSvg from "../../../assets/prevButton.svg";
import HeaderText from "./mainTextOfPage/MainTextOfPage";
import { QuestionData } from "../api/getRequestion";

export const Questionnaire = () => {
  const navigate = useNavigate();
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [data, setData] = useState<QuestionData | null>(null);
  const [answers, setAnswers] = useState<(number | null)[]>([]);

  useEffect(() => {
    const loadQuestions = async () => {
      try {
        const fetchedData = await fetchQuestions(1, 4, 'query_id=AAHWFXQpAAAAANYVdCneE7xN&user=%7B%22id%22%3A695473622%2C%22first_name%22%3A%22Nikita%22%2C%22last_name%22%3A%22Gilevski%22%2C%22username%22%3A%22tla_nnn%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1730365521&hash=f1d40108f106a78c332fa12eb83918ef674aa934cc5b5cea8b2fd17bbe40a15e');

        setData(fetchedData);
        setAnswers(Array(fetchedData.total).fill(null));
      } catch (err) {
        console.error(err);
      }
    };

    loadQuestions();
  }, []);

  const handleNextQuestion = () => {
    if (currentQuestionIndex < (data?.total ?? 0) - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      console.log(answers);
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
    newAnswers[currentQuestionIndex] = newAnswers[currentQuestionIndex] === index ? null : index;
    setAnswers(newAnswers);
  };

  if (!data) {
    return <div>Загрузка...</div>;
  }

  return (
    <>
      <Header />
      <div>
        <HeaderText text={"Выберите утверждение, которое вам ближе"} />
      </div>

      <div className={styles.divForCountOfQuestion}>
        <p>
          {data.page}/{data.pages}
        </p>
      </div>
      <hr className={styles.hr} />

      <div className={styles.divForAnswer}>
        {data.items?.map((question, index) => (
          <CircleToggle
            key={question.id}
            text={question.name}
            isFilled={answers[currentQuestionIndex] === index}
            onSelect={() => handleAnswerSelect(index)}
          />
        ))}
      </div>

      <div className={styles.buttonContainer}>
        {currentQuestionIndex > 0 && (
          <button className={styles.prevButton} onClick={handlePreviousQuestion}>
            <img src={prevButtonSvg} alt="Назад" />
          </button>
        )}
        <button
          className={styles.nextButton}
          onClick={handleNextQuestion}
        >
          Далее
        </button>
      </div>
    </>
  );
};

export default Questionnaire;
