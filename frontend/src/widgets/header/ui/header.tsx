import styles from "./header.module.scss";
import Logo from "../../../assets/kodeLogo.svg";

export const Header = () => {
  return (
    <header className={styles.header}>
			<div>
				<img src={Logo} alt="" />
				<hr className={styles.hr} />
			</div>
    </header>
  );
};

export default Header;
