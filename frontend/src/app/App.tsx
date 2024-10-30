import { Providers } from "./providers";
import { AppRouter } from "./routers";

const App = () => {
  return (
    <Providers>
      <AppRouter />
    </Providers>
  );
};

export default App;
