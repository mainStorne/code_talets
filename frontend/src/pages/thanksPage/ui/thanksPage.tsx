import Net from "../../questionnaire/ui/net/Net";
import styles from "./thankspage.module.scss";

export const ThanksPage = () => {
  return (
    <>
      <Net />
      <h1 className={styles.thanks}>Спасибо что заполнили форму</h1>
      <h2 className={styles.message}>
        Мы обязательно с вами свяжемся больше информации можно увидеть в нашей
        группе
      </h2>
    </>
  );
};

export default ThanksPage;
