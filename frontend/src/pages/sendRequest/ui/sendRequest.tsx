import { useState } from "react";
import { useMutation } from "@tanstack/react-query"; // Importing useMutation from TanStack Query
import styles from "./sendRequests.module.scss";
import { postResumes } from "../../../shared/api/resumes";
import { UserData } from "../../../shared/api/resumes/resumes";

interface PostResumesResponse {
  user: {
    first_name: string;
    middle_name: string;
    last_name: string;
    age: number;
    city: string;
    work_experience: string;
  };
}

export const SendRequest = () => {
  const [fullName, setFullName] = useState("");
  const [age, setAge] = useState<number | undefined>(undefined);
  const [city, setCity] = useState("");
  const [workExperience, setWorkExperience] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const mutation = useMutation<PostResumesResponse, Error, UserData>({
    mutationFn: async (userData: UserData) => {
      const response = await postResumes(userData);
      return response;
    },
    onSuccess: (response) => {
      console.log("Данные успешно отправлены:", response);
      setSuccessMessage("Данные успешно отправлены!");
      setErrorMessage("");
    },
    onError: (error) => {
      console.error("Ошибка при отправке данных:", error);
      setErrorMessage("Произошла ошибка. Попробуйте снова.");
      setSuccessMessage("");
    },
  });

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();

    const [first_name, middle_name, last_name] = fullName.split(" ");

    const userData: UserData = {
      first_name,
      middle_name,
      last_name,
      age,
      city,
      work_experience: workExperience,
    };

    mutation.mutate(userData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h1 className={styles.title}>Заполните форму</h1>
      <div className={styles.input_container}>
        <label htmlFor="name">
          Как вас зовут (ФИО) <span>*</span>
        </label>
        <input
          className={styles.input}
          type="text"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          required
        />
      </div>
      <div className={styles.input_container}>
        <label htmlFor="age">
          Возраст <span>*</span>
        </label>
        <input
          className={styles.input}
          type="number"
          value={age}
          onChange={(e) => setAge(Number(e.target.value))}
          required
        />
      </div>
      <div className={styles.input_container}>
        <label htmlFor="city">
          Город <span>*</span>
        </label>
        <input
          className={styles.input}
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          required
        />
      </div>
      <div className={styles.input_container}>
        <label htmlFor="workExperience">
          Опыт работы <span>*</span>
        </label>
        <input
          className={styles.big_input}
          type="text"
          value={workExperience}
          onChange={(e) => setWorkExperience(e.target.value)}
          required
        />
      </div>

      <div className={styles.input_container}>
        <label htmlFor="resume">
          Резюме <span>*</span>
        </label>
        <label htmlFor="resume" className={styles.upload_button}>
          Добавить файл
        </label>
        <input id="resume" className={styles.hidden_input} type="file" />
      </div>

      <h2 className={styles.sopd}>
        Максимальный размер файла - 50МБ. Допустимые форматы - txt, pdf, doc,
        docx, xls, xlsx, ppt, pptx, bmp, gif, jpg, jpeg, png, zip, rar.
      </h2>
      <label className={styles.custom_checkbox}>
        <input type="checkbox" name="checkbox" required />
        <span></span>
        <h3 className={styles.checkbox_text}>
          Я прочитал(а) политику обработки персональных данных и даю согласие на
          обработку своих данных
        </h3>
      </label>

      {successMessage && <p className={styles.success}>{successMessage}</p>}
      {errorMessage && <p className={styles.error}>{errorMessage}</p>}
      <button type="submit">Отправить</button>
    </form>
  );
};

export default SendRequest;
