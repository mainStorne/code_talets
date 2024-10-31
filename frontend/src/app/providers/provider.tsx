import { FC } from "react";
import { Provider } from "react-redux";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import store from "../store";

interface IProviders {
  readonly children: JSX.Element;
}

// Создайте экземпляр QueryClient
const queryClient = new QueryClient();

export const Providers: FC<IProviders> = ({ children }) => {
  return (
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </Provider>
  );
};
