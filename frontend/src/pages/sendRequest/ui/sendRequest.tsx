import styles from "./sendRequests.module.scss";

export const SendRequest = () => {
  return (
    <>
      <h1 className={styles.title}>Заполните форму</h1>
      <div className={styles.input_container}>
        <label htmlFor="name">Как вас зовут (ФИО)</label>
        <input className={styles.input} type="text" />
      </div>
      <div className={styles.input_container}>
        <label htmlFor="age">Возраст</label>
        <input className={styles.input} type="number" />
      </div>
      <div className={styles.input_container}>
        <label htmlFor="city">Город</label>
        <input className={styles.input} type="text" />
      </div>
      <div className={styles.input_container}>
        <label htmlFor="city">Опыт работы</label>
        <input className={styles.big_input} type="text" />
      </div>

      <div className={styles.input_container}>
        <label htmlFor="resume" className={styles.upload_button}>
          Добавить файл
        </label>
        <input id="resume" className={styles.hidden_input} type="file" />
      </div>
      <h2>
        Макимальный размер файла - 50МБ. Допустимые форматы - txt, pdf, doc,
        docx, xis, xIsx, ppt, pptx, bmp, gif, jpg, jpeg, png, zip, rar.
      </h2>
    </>
  );
};

export default SendRequest;
