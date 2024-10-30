import styles from "./header.module.scss";
import Logo from "../../../assets/kodeLogo.svg";

export const Header = () => {
  return (
    <header className={styles.header}>
      <img src={Logo} alt="" />
    </header>
  );
};

export default Header;
