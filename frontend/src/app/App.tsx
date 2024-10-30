import { Providers } from "./providers/providers";
import { AppRouter } from "./router";

const App = () => {
  return (
    <Providers>
      <AppRouter />
    </Providers>
  );
};

export default App;
