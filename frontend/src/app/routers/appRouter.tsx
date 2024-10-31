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
import { WelcomeTest } from "../../pages/questionnaire/ui/WelcomeTest";
import { AnswerTest } from "../../pages/questionnaire/ui/AnswerTest";
import { ThanksPage } from "../../pages/thanksPage";
import { SendTestPage } from "../../pages/sendTestPage";
import { SendAnswer } from "../../pages/sendAnswer/ui/sendAnswer";

export const AppRouter = () => {
  const routers = createRoutesFromElements(
    <Route path="/" element={<Layout />}>
      <Route path="/send_request" element={<SendRequest />} />
      <Route path="/welcome_test" element={<WelcomeTest />} />
      <Route path="/answer_test" element={<AnswerTest />} />
      <Route path="/test" element={<Questionnaire />} />
      <Route path="/thank_you" element={<ThanksPage />} />
      <Route path="/send_answer/:id" element={<SendAnswer />} />
      <Route path="/send_test/:id" element={<SendTestPage />} />
      {/* <Route path="/send_test" element={<SendTestPage />} /> */}
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
