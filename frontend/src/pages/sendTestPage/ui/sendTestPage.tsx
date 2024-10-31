import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  useQuery,
  useMutation,
  UseMutationResult,
} from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { getUserData } from "../../../shared/api/getResumes";
import { postCase } from "../../../shared/api/sendTestEx/";
import styles from "./sendtestpage.module.scss";

// Define the interface for the case data
interface CaseData {
  case_url: string;
  text: string;
  creator_id: number;
  executor_id: number;
  exp_at: string;
}

export const SendTestPage = () => {
	const navigate = useNavigate()
  const { id } = useParams<{ id: string }>();
  const initData = window.Telegram.WebApp.initData;

  const [executionTime, setExecutionTime] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [fileLink, setFileLink] = useState<string>("");
  const [isFormValid, setIsFormValid] = useState(false);

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
			console.log(response);
      navigate("/thank_you")
    },
    onError: (error) => {
      console.error("Error submitting case:", error);
    },
  });

  useEffect(() => {
    setIsFormValid(
      executionTime.trim().length > 0 &&
        description.trim().length > 0 &&
        fileLink.trim().length > 0
    );
  }, [executionTime, description, fileLink]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const caseData: CaseData = {
      case_url: fileLink,
      text: description,
      creator_id: data?.id || 0,
      executor_id: Number(id),
      exp_at: new Date(executionTime).toISOString(),
    };

    mutation.mutate(caseData);
  };

  if (isLoadingUser) return <p>Loading...</p>;
  if (error) return <p>Произошла ошибка: {error.message}</p>;

  return (
    <>
      <h1 className={styles.name}>
        {data?.first_name} {data?.middle_name} {data?.last_name}
      </h1>
      <hr className={styles.hre} />
      <h2>
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
        Резюме:
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

      <h1 className={styles.name}>Заполните форму</h1>
      <form onSubmit={handleSubmit}>
        <div className={styles.input_container}>
          <label htmlFor="executionTime">
            Дата окончания <span>*</span>
          </label>
          <input
            className={styles.input}
            type="date"
            id="executionTime"
            value={executionTime}
            onChange={(e) => setExecutionTime(e.target.value)}
            required
          />
        </div>
        <div className={styles.input_container}>
          <label htmlFor="description">
            Описание задания и рекомендации <span>*</span>
          </label>
          <input
            className={styles.input}
            type="text"
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>
        <div className={styles.input_container}>
          <label htmlFor="fileLink">
            Тестовое задание (ссылка) <span>*</span>
          </label>
          <input
            className={styles.input}
            type="text"
            id="fileLink"
            value={fileLink}
            onChange={(e) => setFileLink(e.target.value)}
            required
          />
        </div>
        {mutation.isError && (
          <p className={styles.error}>
            Произошла ошибка при отправке: {mutation.error.message}
          </p>
        )}
        {mutation.isSuccess && (
          <p className={styles.success}>Задание успешно отправлено!</p>
        )}
        <button
          type="submit"
          className={`${styles.submit_button} ${
            !isFormValid ? styles.disabled_button : ""
          }`}
          disabled={!isFormValid}
        >
          Отправить
        </button>
      </form>
    </>
  );
};

export default SendTestPage;
