import { Header } from "../../../widgets/header";
import { useLocation } from 'react-router-dom';
import styles from "./AnswerTest.module.scss";
import HeaderText from "./mainTextOfPage/MainTextOfPage";
import Net from "./net/Net";

interface ResponseOption {
  id: number;
  name: string;
  text: string;
  urls: string;
}

interface ResponseData {
  response: ResponseOption[];
}

export const AnswerTest = () => {
  const location = useLocation();
  const { response } = location.state as ResponseData;

  return (
    <>
      <Net />
      <Header />
      <div>
        <HeaderText text={'Ваш результат:'} />
      </div>

      {response.map((selectedOption) => {

        return (
          <div key={selectedOption.id}>
            <h2 className={styles.DivForMainText}>{selectedOption.name}</h2>
            <div className={styles.DivText}>
							{selectedOption.text.split(/\.\s+/).map((part, index) => (
								<p className={styles.divForText} key={index}>
									{part.trim()}.{index < selectedOption.text.split(/\.\s+/).length - 1 && <br />}
								</p>
							))}
						</div>

            <div className={styles.divForLink}>
              <a className={styles.link} href={selectedOption.urls.split(';')[0]} target="_blank" rel="noopener noreferrer">
                Подробнее
              </a>
            </div>
          </div>
        );
      })}
    </>
  );
};

export default AnswerTest;
