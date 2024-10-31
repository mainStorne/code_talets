import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import styles from "./sendAnswer.module.scss";
import { getUserData } from "../../../shared/api/getResumes/";

export const SendAnswer = () => {
  const { id } = useParams();
  const initData = window.Telegram.WebApp.initData;

  const {
    data: userData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["userData", id],
    queryFn: () => getUserData(Number(id), initData),
    enabled: !!id,
    retry: false,
    refetchOnWindowFocus: false,
  });

  if (isLoading) return <p>Загрузка данных...</p>;
  if (error)
    return <p className={styles.error}>Ошибка загрузки данных пользователя</p>;

  return (
    <>
      <h3 className={styles.mainText}>Bvz</h3>
      <hr className={styles.hre} />
      <h2 className={styles.age}>
        Возраст: <span>{userData?.age || "Нет данных"}</span>
      </h2>
      <h2>
        Город: <span>{userData?.city || "Нет данных"}</span>
      </h2>
      <h2>
        Номер телефона: <span>{userData?.phone_number || "Нет данных"}</span>
      </h2>
      <h2>
        Опыт работы: <span>{userData?.work_experience || "Нет данных"}</span>
      </h2>
      <h2>
        Резюме:
        <span>
          {userData?.resume ? (
            <a
              href={userData.resume.resume_url}
              target="_blank"
              rel="noopener noreferrer"
            >
              Скачать резюме
            </a>
          ) : (
            "Нет данных"
          )}
        </span>
      </h2>
      <hr className={styles.hre} />

      <h3 className={styles.name}>Отправьте задание</h3>
      <p className={styles.time}>
        Осталось Времени:
        <span className={styles.dinamicTime}>{/* Оставшееся время */}</span>
      </p>

      <form>
        <div className={styles.input_container}>
          <label htmlFor="fileLink">
            Ваше тестовое задание (ссылка) <span>*</span>
          </label>
          <input className={styles.input} type="text" id="fileLink" />
        </div>
        <button type="submit" className={styles.submit_button}>
          Отправить
        </button>
      </form>
      <p className={styles.error}>{/* Сообщение об ошибке */}</p>
      <p className={styles.success}>{/* Сообщение об успешной отправке */}</p>
    </>
  );
};

export default SendAnswer;
