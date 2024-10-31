import { useParams } from "react-router-dom";
import { useQuery, useMutation } from "@tanstack/react-query";
import styles from "./sendAnswer.module.scss";
import { getUserData } from "../../../shared/api/getResumes/";
import { PostDoneEx } from "../../../shared/api/answerToTestEx";
import { useState } from "react";

export const SendAnswer = () => {
  const { id } = useParams();
  const initData = window.Telegram.WebApp.initData;
  const [fileLink, setFileLink] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

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

  const mutation = useMutation({
    mutationFn: (fileLink: string) =>
      PostDoneEx(initData, {
        case_url: fileLink,
        answer_to_id: Number(id),
      }),
    onSuccess: () => {
      setSuccessMsg("Тестовое задание успешно отправлено!");
      setErrorMsg("");
      setIsSubmitting(false);
    },
    onError: () => {
      setErrorMsg("Ошибка при отправке тестового задания.");
      setSuccessMsg("");
      setIsSubmitting(false);
    },
  });

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    setErrorMsg("");
    setSuccessMsg("");
    if (!fileLink) {
      setErrorMsg("Пожалуйста, укажите ссылку на тестовое задание.");
      return;
    }
    setIsSubmitting(true);
    mutation.mutate(fileLink);
  };

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
        <span className={styles.dinamicTime}></span>
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
            value={fileLink}
            onChange={(e) => setFileLink(e.target.value)}
          />
        </div>
        {errorMsg && <p className={styles.error}>{errorMsg}</p>}
        {successMsg && <p className={styles.success}>{successMsg}</p>}
        <button
          type="submit"
          className={styles.submit_button}
          disabled={isSubmitting}
          style={{ backgroundColor: isSubmitting ? "grey" : undefined }}
        >
          {isSubmitting ? "Загрузка..." : "Отправить"}
        </button>
      </form>
    </>
  );
};

export default SendAnswer;
