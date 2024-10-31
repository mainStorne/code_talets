import { useState } from "react";
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
  start_time: string;
  exp_at: string;
}

export const SendTestPage = () => {
  const { id } = useParams<{ id: string }>();
  const initData = window.Telegram.WebApp.initData;

  // Form state
  const [executionTime, setExecutionTime] = useState<string>("");
  const [description, setDescription] = useState<string>("");
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

  // Mutation for posting case data
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
      text: description,
      creator_id: data?.id || 0,
      executor_id: Number(id),
      start_time: new Date().toISOString(),
      exp_at: executionTime,
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

      <h1 className={styles.name}>Заполните форму</h1>
      <form onSubmit={handleSubmit}>
        <div className={styles.input_container}>
          <label htmlFor="executionTime">
            Дата окончания <span>*</span>
          </label>
          <input
            className={styles.input}
            type="text"
            id="executionTime"
            value={executionTime}
            onChange={(e) => setExecutionTime(e.target.value)}
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
          />
        </div>
        <div className={styles.input_container}>
          <label htmlFor="file">
            Тестовое задание (файл) <span>*</span>
          </label>
          <label htmlFor="file" className={styles.upload_button}>
            Добавить файл
          </label>
          <input
            id="file"
            className={styles.hidden_input}
            type="file"
            onChange={(e) => e.target.files}
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

export default SendTestPage;