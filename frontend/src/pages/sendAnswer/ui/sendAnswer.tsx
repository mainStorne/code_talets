import { useParams } from "react-router-dom";
import { useQuery, useMutation } from "@tanstack/react-query";
import styles from "./sendAnswer.module.scss";
import { getUserData } from "../../../shared/api/getResumes/";
import { PostDoneEx } from "../../../shared/api/answerToTestEx";
import { GetCaseData } from "../../../shared/api/getCasesId";
import { useState, useEffect } from "react";

export const SendAnswer = () => {
  const { id } = useParams();
  const initData = window.Telegram.WebApp.initData;
  const [fileLink, setFileLink] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [executorId, setExecutorId] = useState<number | null>(null);
  const [expAt, setExpAt] = useState<Date | null>(null);
  const [remainingTime, setRemainingTime] = useState<string>("");

  const {
    data: caseData,
    isLoading: isLoadingCase,
    error: caseError,
  } = useQuery({
    queryKey: ["caseData", id],
    queryFn: () => GetCaseData({ id: Number(id), initData }),
    enabled: !!id,
    retry: false,
    refetchOnWindowFocus: false,
  });

  useEffect(() => {
    if (caseData) {
      const { executor_id, exp_at } = caseData;
      setExecutorId(executor_id);
      setExpAt(new Date(exp_at));
      console.log("Executor ID:", executor_id);
    }
  }, [caseData]);

  useEffect(() => {
    if (expAt) {
      const updateRemainingTime = () => {
        const now = new Date();
        const diff = expAt.getTime() - now.getTime();

        if (diff <= 0) {
          setRemainingTime("Время вышло");
        } else {
          const hours = Math.floor(diff / (1000 * 60 * 60));
          const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
          setRemainingTime(`${hours} ч ${minutes} мин`);
        }
      };

      updateRemainingTime();
      const intervalId = setInterval(updateRemainingTime, 60000);

      return () => clearInterval(intervalId);
    }
  }, [expAt]);

  const {
    data: userData,
    isLoading: isLoadingUser,
    error: userError,
  } = useQuery({
    queryKey: ["userData", executorId],
    queryFn: () => getUserData(Number(executorId), initData),
    enabled: executorId !== null,
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

  if (isLoadingCase) return <p>Загрузка данных дела...</p>;
  if (caseError)
    return <p className={styles.error}>Ошибка загрузки данных дела</p>;

  if (isLoadingUser) return <p>Загрузка данных пользователя...</p>;
  if (userError)
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
        <span className={styles.dinamicTime}>{remainingTime}</span>
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
        <button className={styles.button} type="submit" disabled={isSubmitting}>
          Отправить
        </button>
      </form>
    </>
  );
};
