import { Outlet } from "react-router-dom";
import { Header } from "../../widgets/header";
import styles from "./layout.module.scss";

export const Layout = () => {
  return (
    <div className={styles.layout}>
      <Header />

      <main className={styles.layout__content}>
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
