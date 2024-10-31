import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom"; // Import useParams
import { getUserData } from "../../../shared/api/getResumes";
import styles from "./sendtestpage.module.scss";

export const SendTestPage = () => {
  const { id } = useParams<{ id: string }>();
  const initData = window.Telegram.WebApp.initData;

  const { data, error, isLoading } = useQuery({
    queryKey: ["userData", id, initData],
    queryFn: () => getUserData(Number(id), initData),
    enabled: !!id,
  });

  if (isLoading) return <p>Loading...</p>;
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
      <div className={styles.input_container}>
        <label htmlFor="time">
          Время выполнения <span>*</span>
        </label>
        <input className={styles.input} type="text" />
      </div>
      <div className={styles.input_container}>
        <label htmlFor="description">
          Описание задания и рекомендации <span>*</span>
        </label>
        <input className={styles.input} type="text" />
      </div>
      <div className={styles.input_container}>
        <label htmlFor="resume">
          Тестовое задание (файл) <span>*</span>
        </label>
        <label htmlFor="resume" className={styles.upload_button}>
          Добавить файл
        </label>
        <input id="resume" className={styles.hidden_input} type="file" />
      </div>
      <div className={styles.input_container}>
        <label htmlFor="link">
          Тестовое задание (ссылка) <span>*</span>
        </label>
        <input className={styles.input} type="text" />
      </div>
      <button
        type="submit"
        className={`${styles.submit_button} ${styles.inactive_button}`}
      >
        Отправить
      </button>
    </>
  );
};

export default SendTestPage;
