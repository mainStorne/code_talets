import styles from "./AnswerTest.module.scss";
import { Header } from "../../../widgets/header";
import HeaderText from "./mainTextOfPage/MainTextOfPage";

export const WelcomeTest = () => {

  return (
    <>
      <Header />
      <div>
				<HeaderText text={'Ваш результат:'} />
      </div>

      <div className={styles.mainText}>
				<p>
					В сфере разработки существует множество направлений, в том числе не связанных с языками программирования.
				</p>

				<p className={styles.text}>
					Пройдите тест и узнайте, какие профессии в IT подходят именно вам.
        </p>
      </div>
    </>
  );
};

export default WelcomeTest;
