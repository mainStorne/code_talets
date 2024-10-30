import { Outlet } from "react-router-dom";
import styles from "./layout.module.scss";
import { Header } from "../../widgets/header";

export const Layout = () => {
  return (
    <div className={`${styles.layout} ${styles.layout__wrapper}`}>
      <Header />
      <main className={styles.layout__content}>
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
