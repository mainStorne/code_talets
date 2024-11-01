import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { useFormik } from "formik";
import * as Yup from "yup";
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
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const mutation = useMutation<PostResumesResponse, Error, UserData>({
    mutationFn: async (userData: UserData) => {
      const response = await postResumes(userData, file || undefined);
      return response;
    },
    onSuccess: (response) => {
      console.log("Данные успешно отправлены:", response);
      setIsSubmitting(false);
      if (nextParam) {
        navigate("/welcome_test");
      } else {
        navigate("/thank_you");
      }
    },
    onError: (error) => {
      console.error("Ошибка при отправке данных:", error);
      setIsSubmitting(false);
    },
  });

  const formik = useFormik({
    initialValues: {
      fullName: "",
      age: "",
      city: "",
      workExperience: "",
      phoneNumber: "",
      checkbox: false,
    },
    validationSchema: Yup.object({
      fullName: Yup.string()
        .matches(/^[a-zA-Zа-яА-Я\s]+$/, "Введите корректные ФИО")
        .required("Обязательное поле"),
      age: Yup.number()
        .required("Обязательное поле")
        .positive("Возраст должен быть положительным числом")
        .integer("Возраст должен быть целым числом"),
      city: Yup.string().required("Обязательное поле"),
      workExperience: Yup.string().required("Обязательное поле"),
      phoneNumber: Yup.string().required("Обязательное поле"),
      checkbox: Yup.boolean().oneOf(
        [true],
        "Вы должны принять политику обработки персональных данных"
      ),
    }),
    onSubmit: (values) => {
      setIsSubmitting(true);
      const [first_name, middle_name, last_name] = values.fullName.split(" ");
      const userData: UserData = {
        first_name,
        middle_name,
        last_name,
        age: Number(values.age),
        city: values.city,
        work_experience: values.workExperience,
        phone_number: values.phoneNumber,
      };
      mutation.mutate(userData);
    },
  });

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
    }
  };

  return (
    <form onSubmit={formik.handleSubmit}>
      <h1 className={styles.title}>Заполните форму</h1>
      <div className={styles.input_container}>
        <label htmlFor="fullName">
          Как вас зовут (ФИО) <span>*</span>
        </label>
        <input
          className={styles.input}
          placeholder="Иванов Иван Иванович"
          type="text"
          id="fullName"
          {...formik.getFieldProps("fullName")}
        />
        {formik.touched.fullName && formik.errors.fullName ? (
          <div className={styles.error}>{formik.errors.fullName}</div>
        ) : null}
      </div>
      <div className={styles.input_container}>
        <label htmlFor="age">
          Возраст <span>*</span>
        </label>
        <input
          className={styles.input}
          type="number"
          id="age"
          {...formik.getFieldProps("age")}
        />
        {formik.touched.age && formik.errors.age ? (
          <div className={styles.error}>{formik.errors.age}</div>
        ) : null}
      </div>
      <div className={styles.input_container}>
        <label htmlFor="city">
          Город <span>*</span>
        </label>
        <input
          className={styles.input}
          type="text"
          id="city"
          {...formik.getFieldProps("city")}
        />
        {formik.touched.city && formik.errors.city ? (
          <div className={styles.error}>{formik.errors.city}</div>
        ) : null}
      </div>
      <div className={styles.input_container}>
        <label htmlFor="phoneNumber">
          Номер телефона <span>*</span>
        </label>
        <InputMask
          className={styles.input}
          mask="+7 (999) 999-99-99"
          id="phoneNumber"
          {...formik.getFieldProps("phoneNumber")}
        />
        {formik.touched.phoneNumber && formik.errors.phoneNumber ? (
          <div className={styles.error}>{formik.errors.phoneNumber}</div>
        ) : null}
      </div>
      <div className={styles.input_container}>
        <label htmlFor="workExperience">
          Опыт работы <span>*</span>
        </label>
        <input
          className={styles.big_input}
          type="text"
          id="workExperience"
          {...formik.getFieldProps("workExperience")}
        />
        {formik.touched.workExperience && formik.errors.workExperience ? (
          <div className={styles.error}>{formik.errors.workExperience}</div>
        ) : null}
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
          !formik.values.checkbox ? styles.inactive_checkbox : ""
        }`}
      >
        <input
          type="checkbox"
          id="checkbox"
          {...formik.getFieldProps("checkbox")}
        />
        <span></span>
        <h3 className={styles.checkbox_text}>
          Я прочитал(а) политику обработки персональных данных и даю согласие на
          обработку своих данных
        </h3>
      </label>
      {formik.errors.checkbox && formik.touched.checkbox ? (
        <div className={styles.error}>{formik.errors.checkbox}</div>
      ) : null}
      <button
        type="submit"
        className={`${styles.submit_button} ${
          !formik.isValid || isSubmitting ? styles.inactive_button : ""
        }`}
        disabled={!formik.isValid || isSubmitting}
      >
        {isSubmitting ? "Отправка..." : "Отправить"}
      </button>
      {mutation.isError && (
        <div className={styles.error}>
          Произошла ошибка: {mutation.error?.message}
        </div>
      )}
      {mutation.isSuccess && (
        <div className={styles.success}>Данные успешно отправлены!</div>
      )}
    </form>
  );
};

export default SendRequest;
