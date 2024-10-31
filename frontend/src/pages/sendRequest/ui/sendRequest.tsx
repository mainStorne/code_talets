import { useState, useEffect } from "react";
import { useMutation } from "@tanstack/react-query";
import styles from "./sendRequests.module.scss";
import { postResumes } from "../../../shared/api/resumes";
import { UserData } from "../../../shared/api/resumes/resumes";
import { useNavigate, useLocation } from "react-router-dom";
import InputMask from "react-input-mask";

interface PostResumesResponse {
  user: {
    first_name: string;
    middle_name: string;
    last_name: string;
    age: number;
    city: string;
    work_experience: string;
    phone_number: string;
  };
}

export const SendRequest = () => {
  const location = useLocation();
  const nextParam = new URLSearchParams(location.search).get("next");
  const [fullName, setFullName] = useState("");
  const [age, setAge] = useState<number | undefined>(undefined);
  const [city, setCity] = useState("");
  const [workExperience, setWorkExperience] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [isFormValid, setIsFormValid] = useState(false);
  const [isCheckboxChecked, setIsCheckboxChecked] = useState(false);
  const navigate = useNavigate();

  const mutation = useMutation<PostResumesResponse, Error, UserData>({
    mutationFn: async (userData: UserData) => {
      const response = await postResumes(userData, file || undefined);
      return response;
    },
    onSuccess: (response) => {
      console.log("Данные успешно отправлены:", response);
      setSuccessMessage("Данные успешно отправлены!");
      setErrorMessage("");
      if (nextParam) {
        navigate("/welcome_test");
      } else {
        navigate("/thank_you");
      }
    },
    onError: (error) => {
      console.error("Ошибка при отправке данных:", error);
      setErrorMessage("Произошла ошибка. Попробуйте снова.");
      setSuccessMessage("");
    },
  });

  useEffect(() => {
    const isValid =
      fullName.trim().split(" ").length === 3 &&
      age !== undefined &&
      age > 0 &&
      city.trim().length > 0 &&
      workExperience.trim().length > 0 &&
      phoneNumber.trim().length > 0 &&
      file !== null &&
      isCheckboxChecked;

    setIsFormValid(isValid);
  }, [
    fullName,
    age,
    city,
    workExperience,
    phoneNumber,
    file,
    isCheckboxChecked,
  ]);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const [first_name, middle_name, last_name] = fullName.split(" ");

    const userData: UserData = {
      first_name,
      middle_name,
      last_name,
      age,
      city,
      work_experience: workExperience,
      phone_number: phoneNumber,
    };

    mutation.mutate(userData);
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
    }
  };

  const handleCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setIsCheckboxChecked(event.target.checked);
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
          placeholder="Иванов Иван Иванович"
          type="text"
          value={fullName}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setFullName(e.target.value)
          }
          required
        />
        <label htmlFor="name"></label>
      </div>
      <div className={styles.input_container}>
        <label htmlFor="age">
          Возраст <span>*</span>
        </label>
        <input
          className={styles.input}
          type="number"
          value={age}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setAge(Number(e.target.value))
          }
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
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setCity(e.target.value)
          }
          required
        />
      </div>
      <div className={styles.input_container}>
        <label htmlFor="phone">
          Номер телефона <span>*</span>
        </label>
        <InputMask
          className={styles.input}
          mask="+7 (999) 999-99-99"
          value={phoneNumber}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setPhoneNumber(e.target.value)
          }
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
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setWorkExperience(e.target.value)
          }
          required
        />
      </div>

      <div className={styles.input_container}>
        <label htmlFor="resume">
          Резюме <span>*</span>
        </label>
        <label htmlFor="resume" className={styles.upload_button}>
          {fileName || "Добавить файл"}
        </label>
        <input
          id="resume"
          className={styles.hidden_input}
          type="file"
          onChange={handleFileChange}
        />
      </div>

      <h2 className={styles.sopd}>
        Максимальный размер файла - 50МБ. Допустимые форматы - txt, pdf, doc,
        docx, xls, xlsx, ppt, pptx, bmp, gif, jpg, jpeg, png, zip, rar.
      </h2>
      <label
        className={`${styles.custom_checkbox} ${
          !isFormValid ? styles.inactive_checkbox : ""
        }`}
      >
        <input
          type="checkbox"
          name="checkbox"
          required
          checked={isCheckboxChecked}
          onChange={handleCheckboxChange}
        />
        <span></span>
        <h3 className={styles.checkbox_text}>
          Я прочитал(а) политику обработки персональных данных и даю согласие на
          обработку своих данных
        </h3>
      </label>

      {successMessage && <p className={styles.success}>{successMessage}</p>}
      {errorMessage && <p className={styles.error}>{errorMessage}</p>}
      <button
        type="submit"
        className={`${styles.submit_button} ${
          !isFormValid ? styles.inactive_button : ""
        }`}
        disabled={!isFormValid}
      >
        Отправить
      </button>
    </form>
  );
};

export default SendRequest;
