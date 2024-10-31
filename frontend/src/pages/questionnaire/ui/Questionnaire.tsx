import { useState, useEffect } from "react";
import styles from "./Questionnaire.module.scss";
import { Header } from "../../../widgets/header";
import CircleToggle from "./circleToggle/CircleToggle";
import { fetchQuestions } from "../../../shared/api/profTest/getRequestion";
import { useNavigate } from "react-router-dom";
import prevButtonSvg from "../../../assets/prevButton.svg";
import HeaderText from "./mainTextOfPage/MainTextOfPage";
import { useLoad } from '../../../app/providers/load/loadProvider';
import Loading from '../../../widgets/loading/ui/loading';
import { QuestionData } from "../../../shared/api/profTest/getRequestion";
import { sendAnswers } from "../../../shared/api/profTest/sendAnswers";

export const Questionnaire = () => {
	const initData = window.Telegram.WebApp.initData;
  const { setLoading } = useLoad();
  const navigate = useNavigate();
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [data, setData] = useState<QuestionData | null>(null);
  const [answers, setAnswers] = useState<(number | null)[]>([]);
  const [speciality_id, setSpecialityId] = useState<number[]>([]);

  useEffect(() => {
    const loadQuestions = async () => {
      setLoading(true);
      await fetchAndSetQuestions(currentQuestionIndex + 1);
      setLoading(false);
    };

    loadQuestions();
  }, [currentQuestionIndex]);

  const fetchAndSetQuestions = async (page: number) => {
    try {
      const fetchedData = await fetchQuestions(page, 4, initData);

      const newAnswers = [...answers];
      if (fetchedData.total) {
        for (let i = 0; i < fetchedData.total; i++) {
          if (newAnswers.length <= currentQuestionIndex + i) {
            newAnswers[currentQuestionIndex + i] = null;
          }
        }
      }

      if (fetchedData.items) {
        for (let i = 0; i < fetchedData.items.length; i++) {
          if (newAnswers[currentQuestionIndex + i] === undefined) {
            newAnswers[currentQuestionIndex + i] = null;
          }
        }
      }

      setData(fetchedData);
      setAnswers(newAnswers);
    } catch (err) {
      console.error("Error fetching questions:", err);
    }
  };

  const handleNextQuestion = async () => {
    if (answers[currentQuestionIndex] === null) {
      return;
    }

    if (currentQuestionIndex < (data?.pages ?? 0) - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      try {
        setLoading(true);
        const response = await sendAnswers(speciality_id, initData);
        setLoading(false);
        navigate("/answer_test", { state: { response } });
      } catch (error) {
        console.error("Error sending answers:", error);
        setLoading(false);
      }
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleAnswerSelect = (index: number) => {
    const newAnswers = [...answers];
    const newSpecialities = [...speciality_id];

    if (data && data.items) {
      const specialityId = data.items[index].speciality_id;

      newAnswers[currentQuestionIndex] = index;
      newSpecialities[currentQuestionIndex] = specialityId;
    }
    setAnswers(newAnswers);
    setSpecialityId(newSpecialities);
  };

  if (!data || !data.items) {
    return <Loading />;
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
        {data.items.map((question, index) => {
          return (
            <CircleToggle
              key={question.id}
              text={question.name}
              isFilled={answers[currentQuestionIndex] === index}
              onSelect={() => handleAnswerSelect(index)}
            />
          );
        })}
      </div>

      <div className={styles.buttonContainer}>
        {currentQuestionIndex > 0 && (
          <button
            className={styles.prevButton}
            onClick={handlePreviousQuestion}
          >
            <img src={prevButtonSvg} alt="" />
          </button>
        )}
        <button
          className={
            currentQuestionIndex === 0
              ? styles.nextButton
              : styles.nextButtonSolo
          }
          onClick={handleNextQuestion}
        >
          Далее
        </button>
      </div>
    </>
  );
};

export default Questionnaire;
