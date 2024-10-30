import styles from "./WelcomeTest.module.scss";
import {useNavigate} from "react-router-dom"
import { Header } from "../../../widgets/header";
import HeaderText from "./mainTextOfPage/MainTextOfPage";
import Net from "./net/Net";

export const WelcomeTest = () => {
	const navigate = useNavigate()

  return (
    <>
			<Net />
			<div className={styles.mainDiv}>
				<Header />
				<div>
					<HeaderText text={'Какое направление в IT выбрать?'} />
				</div>
				<div className={styles.mainText}>
					<p>
						В сфере разработки существует множество направлений, в том числе не связанных с языками программирования.
					</p>

					<p className={styles.text}>
						Пройдите тест и узнайте, какие профессии в IT подходят именно вам.
					</p>
				</div>

				<div className={styles.buttonContainer}>
					<button className={styles.startButton} onClick={() => navigate('/test')}>
						Начать
					</button>
				</div>
			</div>
    </>
  );
};

export default WelcomeTest;
