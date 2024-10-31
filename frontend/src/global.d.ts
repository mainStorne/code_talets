interface TelegramWebApp {
  initData: string;
  requestContact(
    callback: (result: { user?: { phone_number?: string } } | null) => void
  ): void;
}

interface Window {
  Telegram: {
    WebApp: TelegramWebApp;
  };
}
