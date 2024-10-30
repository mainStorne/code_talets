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
        <label htmlFor="resume">Резюме</label>
        <input className={styles.resume} type="text" />
      </div>
    </>
  );
};

export default SendRequest;
