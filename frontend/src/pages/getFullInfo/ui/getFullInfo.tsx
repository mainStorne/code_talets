import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import CircleToggle from "../../questionnaire/ui/circleToggle/CircleToggle";
import styles from "./getfullinfo.module.scss";
import { getFull } from "../../../shared/api/getFull"; // Замените на актуальный путь к функции getFull

// // Интерфейсы для данных
// interface UserInfo {
//   first_name: string;
//   last_name: string;
//   age: number;
//   city: string;
//   phone_number: string;
//   work_experience: string;
// }

// interface UserResume {
//   resume_url: string;
// }

// interface CaseAnswer {
//   case_url: string;
// }

export const GetFullInfo = () => {
  const [selectedOption, setSelectedOption] = useState("");

  const { id } = useParams<{ id: string }>();

  const initData = window.Telegram.WebApp.initData;

  const { data, isLoading, error } = useQuery({
    queryKey: ["userCase", id],
    queryFn: () => getFull(Number(id), initData),

    enabled: !!id,
  });

  const handleSelect = (text: string) => {
    setSelectedOption(text);
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
      <button className={styles.submit_button} type="submit">
        Отправить
      </button>
    </>
  );
};

export default GetFullInfo;
