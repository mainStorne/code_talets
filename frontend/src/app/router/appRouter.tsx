import { Layout } from "../layout";
import styles from "../styles/app.module.scss";

import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";

export const AppRouter = () => {
  const routes = createRoutesFromElements(
    <Route path="/" element={<Layout />}>
      <Route path="/books" element />
      <Route path="/products" />
      <Route path="/clients" />
    </Route>
  );

  const router = createBrowserRouter(routes);

  return (
    <div className={styles.app}>
      <RouterProvider router={router} />
    </div>
  );
};
