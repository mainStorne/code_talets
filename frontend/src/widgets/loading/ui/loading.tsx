import styles from "./loading.module.scss";
import Logo from "../../../assets/kodeLogo.svg";

export const Loading = () => {
  return (
		<div className={styles.imgBack}>
			<img className={styles.logo} src={Logo} alt="" />
		</div>
  );
};

export default Loading;
