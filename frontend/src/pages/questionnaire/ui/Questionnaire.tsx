import styles from "./Questionnaire.module.scss";
import { Header } from "../../../widgets/header";


export const Questionnaire = () => {
  return (
    <>
			<Header />
			<div>
				<h2 className={styles.mainTextOfTest}>Выберите утверждение, которое вам ближе</h2>
			</div>

			<div className={styles.divForCountOfQuestion}>
				<p>1/5</p>
			</div>
			<hr  className={styles.hr}/>
    </>
  );
};

export default Questionnaire;
