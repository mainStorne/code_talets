import styles from "./sendRequests.module.scss";

export const SendRequest = () => {
  return (
    <>
      <h1 className={styles.title}>Заполните форму</h1>
      <div className={styles.input_container}>
        <label htmlFor="name">Как вас зовут (ФИО)</label>
        <input type="text" />
      </div>
      <div className={styles.input_container}>
        <label htmlFor="name">Как вас зовут (ФИО)</label>
        <input type="text" />
      </div>
    </>
  );
};

export default SendRequest;
