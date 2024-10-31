import { useState, useEffect } from "react";
import {
  useQuery,
  useMutation,
  UseMutationResult,
} from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { getUserData } from "../../../shared/api/getResumes";
import { postCase } from "../../../shared/api/sendTestEx/";
import styles from "./sendAnswer.module.scss";

interface CaseData {
  case_url: string;
  creator_id: number;
  executor_id: number;
  start_time: string;
}

export const SendAnswer = () => {
  const { id } = useParams<{ id: string }>();
  const initData = window.Telegram.WebApp.initData;
	const [timeRemaining, setTimeRemaining] = useState({ days: 0, hours: 0, minutes: 0, seconds: 0 });

  const [fileLink, setFileLink] = useState<string>("");

  const {
    data,
    error,
    isLoading: isLoadingUser,
  } = useQuery({
    queryKey: ["userData", id, initData],
    queryFn: () => getUserData(Number(id), initData),
    enabled: !!id,
  });

  const mutation: UseMutationResult<unknown, Error, CaseData> = useMutation({
    mutationFn: (caseData: CaseData) => postCase(initData, caseData),
    onSuccess: (response) => {
      console.log("Case posted successfully:", response);
    },
    onError: (error) => {
      console.error("Error submitting case:", error);
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const caseData: CaseData = {
      case_url: fileLink,
      creator_id: data?.id || 0,
      executor_id: Number(id),
      start_time: new Date().toISOString(),
    };

    mutation.mutate(caseData);
  };

	const calculateTimeRemaining = () => {
    const targetDate = new Date(); // Установите целевую дату
    targetDate.setHours(targetDate.getHours() + 1); // Например, 1 час от текущего времени
    const now = new Date();
    const difference = targetDate.getTime() - now.getTime();

    if (difference > 0) {
      const seconds = Math.floor((difference / 1000) % 60);
      const minutes = Math.floor((difference / 1000 / 60) % 60);
      const hours = Math.floor((difference / (1000 * 60 * 60)) % 24);
      const days = Math.floor(difference / (1000 * 60 * 60 * 24));

      setTimeRemaining({ days, hours, minutes, seconds });
    } else {
      setTimeRemaining({ days: 0, hours: 0, minutes: 0, seconds: 0 }); // Время истекло
    }
  };

	useEffect(() => {
    calculateTimeRemaining();
    const timer = setInterval(calculateTimeRemaining, 1000);

    return () => clearInterval(timer);
  }, []);

  if (isLoadingUser) return <p>Loading...</p>;
  if (error) return <p>Произошла ошибка: {error.message}</p>;

  return (
    <>

      <h3 className={styles.mainText}>
        {data?.first_name} {data?.middle_name} {data?.last_name}
				{/* fjasdlflsaj */}
      </h3>
      <hr className={styles.hre} />
      <h2 className={styles.age}>
        Возраст: <span>{data?.age}</span>
      </h2>
      <h2>
        Город: <span>{data?.city}</span>
      </h2>
      <h2>
        Номер телефона: <span>{data?.phone_number}</span>
      </h2>
      <h2>
        Опыт работы: <span>{data?.work_experience}</span>
      </h2>
      <h2>
        Резюме:{" "}
        <span>
          <a
            href={data?.resume.resume_url}
            target="_blank"
            rel="noopener noreferrer"
          >
            Скачать резюме
          </a>
        </span>
      </h2>
      <hr className={styles.hre} />

      <h3 className={styles.name}>Отправьте задание</h3>
			<p className={styles.time}>
        Осталось Времени:{" "}
        <span className={styles.dinamicTime}>
          {timeRemaining.days}d {timeRemaining.hours}h {timeRemaining.minutes}m {timeRemaining.seconds}s
        </span>
      </p>

      <form onSubmit={handleSubmit}>
        <div className={styles.input_container}>
          <label htmlFor="fileLink">
            Ваше тестовое задание (ссылка) <span>*</span>
          </label>
          <input
            className={styles.input}
            type="text"
            id="fileLink"
            onChange={(e) => setFileLink(e.target.value)}
          />
        </div>
        <button type="submit" className={styles.submit_button}>
          Отправить
        </button>
      </form>
      {mutation.isError && (
        <p className={styles.error}>
          Произошла ошибка при отправке: {mutation.error.message}
        </p>
      )}
      {mutation.isSuccess && (
        <p className={styles.success}>Задание успешно отправлено!</p>
      )}
    </>
  );
};

export default SendAnswer;
