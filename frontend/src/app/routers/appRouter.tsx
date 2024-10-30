import styles from "../styles/index.module.scss";
import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";
import { Layout } from "../layout";
import { SendRequest } from "../../pages/sendRequest";
import { Questionnaire } from "../../pages/questionnaire/ui/Questionnaire";

export const AppRouter = () => {
  const routers = createRoutesFromElements(
    <Route path="/" element={<Layout />}>
      <Route path="/send_request" element={<SendRequest />} />
			<Route path="/test" element={<Questionnaire />} />
    </Route>
  );

  const router = createBrowserRouter(routers);

  return (
    <div className={styles.app}>
      <RouterProvider router={router} />
    </div>
  );
};

export default AppRouter;
