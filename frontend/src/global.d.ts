// globals.d.ts
interface TelegramWebApp {
  initData: string;
  // Добавьте другие свойства и методы, если нужно
}

interface Window {
  Telegram: {
    WebApp: TelegramWebApp;
  };
}
