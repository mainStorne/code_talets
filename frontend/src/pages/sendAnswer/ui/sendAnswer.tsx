import styles from "./sendAnswer.module.scss";

export const SendAnswer = () => {
  return (
    <>
      <h3 className={styles.mainText}>Bvz</h3>
      <hr className={styles.hre} />
      <h2 className={styles.age}>
        Возраст: <span>{/* Возраст пользователя */}</span>
      </h2>
      <h2>
        Город: <span>{/* Город пользователя */}</span>
      </h2>
      <h2>
        Номер телефона: <span>{/* Номер телефона пользователя */}</span>
      </h2>
      <h2>
        Опыт работы: <span>{/* Опыт работы пользователя */}</span>
      </h2>
      <h2>
        Резюме:
        <span>
          <a href="" target="_blank" rel="noopener noreferrer">
            Скачать резюме
          </a>
        </span>
      </h2>
      <hr className={styles.hre} />

      <h3 className={styles.name}>Отправьте задание</h3>
      <p className={styles.time}>
        Осталось Времени:
        <span className={styles.dinamicTime}>{/* Оставшееся время */}</span>
      </p>

      <form>
        <div className={styles.input_container}>
          <label htmlFor="fileLink">
            Ваше тестовое задание (ссылка) <span>*</span>
          </label>
          <input className={styles.input} type="text" id="fileLink" />
        </div>
        <button type="submit" className={styles.submit_button}>
          Отправить
        </button>
      </form>
      <p className={styles.error}>{/* Сообщение об ошибке */}</p>
      <p className={styles.success}>{/* Сообщение об успешной отправке */}</p>
    </>
  );
};

export default SendAnswer;
