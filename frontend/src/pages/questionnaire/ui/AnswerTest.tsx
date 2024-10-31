import styles from "./AnswerTest.module.scss";
import { Header } from "../../../widgets/header";
import HeaderText from "./mainTextOfPage/MainTextOfPage";
import { Developer } from "../api/getAnswerRequestion";
import Net from "./net/Net";

export const AnswerTest = () => {
  const options = [Developer];
  const selectedOption = options[0];
	const textParts = selectedOption.text.split('.').filter(part => part.trim() !== '');

  return (
    <>
			<Net />
      <Header />
      <div>
        <HeaderText text={'Ваш результат:'} />
      </div>

      <div className={styles.DivForMainText}>
        <p>{selectedOption.answer}</p>
      </div>

      <div className={styles.divForText}>
				{textParts.map((part, index) => (
          <p key={index} className={styles.text}>{part.trim()}.</p>
        ))}
      </div>
    </>
  );
};

export default AnswerTest;
