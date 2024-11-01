import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import CircleToggle from "../../questionnaire/ui/circleToggle/CircleToggle";
import styles from "./getfullinfo.module.scss";
import { getFull } from "../../../shared/api/getFull";
import { patchUser } from "../../../shared/api/patchUser/patchUser";

export const GetFullInfo = () => {
  const [selectedOption, setSelectedOption] = useState("");
  const { id } = useParams<{ id: string }>();
  const initData = window.Telegram.WebApp.initData;

  const { data, isLoading, error } = useQuery({
    queryKey: ["userCase", id],
    queryFn: () => getFull(Number(id), initData),
    staleTime: 1000 * 60 * 5,
    enabled: !!id,
  });

  const mutation = useMutation({
    mutationFn: async (updatedStatus: string) => {
      console.log("Отправка запроса patchUser с данными:", {
        status: updatedStatus,
      });
      if (data && data.user) {
        return await patchUser(
          data.user.id,
          { status: updatedStatus },
          initData
        );
      }
    },
    onSuccess: () => {
      alert("Статус обновлен успешно!");
    },
    onError: (error) => {
      console.error("Ошибка обновления статуса:", error);
      alert("Ошибка обновления статуса.");
    },
  });

  const handleSelect = (text: string) => {
    setSelectedOption(text);
    console.log("Выбранный вариант:", text); // Добавление логирования для проверки
  };

  const handleSubmit = async () => {
    console.log(
      "Попытка отправки данных с выбранным вариантом:",
      selectedOption
    );
    mutation.mutate(selectedOption);
  };

  if (isLoading) return <p>Загрузка данных...</p>;
  if (error) return <p>Ошибка загрузки данных.</p>;

  return (
    <>
      <h1 className={styles.name}>
        {data?.user.first_name} {data?.user.last_name}
      </h1>
      <hr className={styles.hre} />
      <h2>
        Возраст: <span>{data?.user.age}</span>
      </h2>
      <h2>
        Город: <span>{data?.user.city}</span>
      </h2>
      <h2>
        Номер телефона: <span>{data?.user.phone_number}</span>
      </h2>
      <h2>
        Опыт работы: <span>{data?.user.work_experience}</span>
      </h2>
      <h2>
        Резюме:
        <span>
          <a
            href={data?.user_resume.resume_url}
            target="_blank"
            rel="noopener noreferrer"
          >
            &nbsp;Скачать резюме
          </a>
        </span>
      </h2>
      <h2>
        Ответ на задание: <span>{data?.case_answer.case_url}</span>
      </h2>
      <hr className={styles.hre} />
      <h1 className={styles.name}>Как вам кандидат?</h1>
      <CircleToggle
        text="Хороший"
        isFilled={selectedOption === "Хороший"}
        onSelect={handleSelect}
      />
      <CircleToggle
        text="Отличный"
        isFilled={selectedOption === "Отличный"}
        onSelect={handleSelect}
      />
      <CircleToggle
        text="Не подходит"
        isFilled={selectedOption === "Не подходит"}
        onSelect={handleSelect}
      />
      <button
        className={styles.submit_button}
        type="button"
        onClick={handleSubmit}
      >
        Отправить
      </button>
    </>
  );
};

export default GetFullInfo;
