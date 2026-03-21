type TelegramWebApp = {
  ready: () => void;
  expand: () => void;
  colorScheme?: "light" | "dark";
  platform?: string;
  setHeaderColor?: (color: string) => void;
  setBackgroundColor?: (color: string) => void;
};

declare global {
  interface Window {
    Telegram?: {
      WebApp?: TelegramWebApp;
    };
  }
}

export function bootstrapTelegramWebApp({
  onThemeResolved,
}: {
  onThemeResolved?: (theme: "dark" | "light") => void;
}) {
  const webApp = window.Telegram?.WebApp;
  if (!webApp) {
    return () => undefined;
  }

  const theme = webApp.colorScheme === "light" ? "light" : "dark";
  webApp.ready();
  webApp.expand();
  webApp.setHeaderColor?.(theme === "dark" ? "#0f0d12" : "#ffffff");
  webApp.setBackgroundColor?.(theme === "dark" ? "#0f0d12" : "#f7f5fb");
  onThemeResolved?.(theme);
  document.documentElement.setAttribute("data-telegram-platform", webApp.platform ?? "unknown");

  return () => undefined;
}
