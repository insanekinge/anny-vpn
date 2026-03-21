import { useEffect, useState } from "react";

import { bootstrapTelegramWebApp } from "./lib/telegram";

type TabId = "home" | "plans" | "profile";
type ThemeMode = "dark" | "light";

const tabs: Array<{ id: TabId; label: string }> = [
  { id: "home", label: "Главная" },
  { id: "plans", label: "Тарифы" },
  { id: "profile", label: "Профиль" },
];

const planCards = [
  {
    name: "Базовый",
    price: "0 ₽",
    perks: ["5 локаций", "1 устройство", "Базовая поддержка"],
  },
  {
    name: "Месячный",
    price: "990 ₽",
    perks: ["40+ локаций", "Высокая скорость", "Быстрый доступ к поддержке"],
  },
  {
    name: "Премиум",
    price: "6 990 ₽",
    perks: ["80+ локаций", "Годовая подписка", "Приоритетная линия поддержки"],
  },
];

export function MiniApp() {
  const [activeTab, setActiveTab] = useState<TabId>("home");
  const [theme, setTheme] = useState<ThemeMode>("dark");

  useEffect(() => {
    const cleanup = bootstrapTelegramWebApp({
      onThemeResolved: (resolvedTheme) => setTheme(resolvedTheme),
    });

    return cleanup;
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  return (
    <div className="miniapp">
      <div className="miniapp__device">
        <header className="miniapp__header">
          <div className="miniapp__header-copy">
            <span className="miniapp__brand">AllyVPN Mini</span>
            <h1 className="miniapp__title">Личный кабинет в Telegram</h1>
            <p className="miniapp__subtitle">
              Управляйте подпиской, поддержкой и профилем без перегрузки бота.
            </p>
          </div>
          <span className="miniapp__status">Связано с ботом</span>
        </header>

        <main className="miniapp__content">
          {activeTab === "home" ? <HomeScreen /> : null}
          {activeTab === "plans" ? <PlansScreen /> : null}
          {activeTab === "profile" ? (
            <ProfileScreen
              theme={theme}
              onToggleTheme={() => setTheme((current) => (current === "dark" ? "light" : "dark"))}
            />
          ) : null}
        </main>

        <nav className="miniapp__tabs" aria-label="Навигация">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              type="button"
              className={`miniapp__tab ${tab.id === activeTab ? "miniapp__tab--active" : ""}`}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>
    </div>
  );
}

function HomeScreen() {
  return (
    <section className="miniapp-section">
      <article className="miniapp-card miniapp-card--hero">
        <span className="miniapp-badge">Mini App</span>
        <h2 className="miniapp-card__title">Всё важное в одном месте</h2>
        <p className="miniapp-card__text">
          Здесь удобно смотреть статус подписки, открывать поддержку, проверять доступ и быстро
          переходить к нужным действиям.
        </p>
        <button type="button" className="miniapp-button miniapp-button--primary">
          Открыть поддержку
        </button>
      </article>

      <div className="miniapp-grid">
        <article className="miniapp-card miniapp-card--compact">
          <span className="miniapp-card__label">Тариф</span>
          <strong className="miniapp-card__value">Премиум на год</strong>
          <span className="miniapp-card__hint">Активен до марта 2027</span>
        </article>
        <article className="miniapp-card miniapp-card--compact">
          <span className="miniapp-card__label">Доступ</span>
          <strong className="miniapp-card__value">Выдан</strong>
          <span className="miniapp-card__hint">Конфиги доступны в Telegram</span>
        </article>
      </div>
    </section>
  );
}

function PlansScreen() {
  return (
    <section className="miniapp-section">
      {planCards.map((plan) => (
        <article
          key={plan.name}
          className={`miniapp-card miniapp-plan ${plan.name === "Премиум" ? "miniapp-plan--featured" : ""}`}
        >
          <div className="miniapp-plan__header">
            <div>
              <h2 className="miniapp-card__title">{plan.name}</h2>
              <p className="miniapp-card__text">Чёткий и понятный выбор без лишних шагов.</p>
            </div>
            <strong className="miniapp-plan__price">{plan.price}</strong>
          </div>

          <ul className="miniapp-plan__list">
            {plan.perks.map((perk) => (
              <li key={perk}>{perk}</li>
            ))}
          </ul>

          <button type="button" className="miniapp-button miniapp-button--primary">
            {plan.name === "Базовый" ? "Текущий тариф" : "Выбрать тариф"}
          </button>
        </article>
      ))}
    </section>
  );
}

function ProfileScreen({
  theme,
  onToggleTheme,
}: {
  theme: ThemeMode;
  onToggleTheme: () => void;
}) {
  return (
    <section className="miniapp-section">
      <article className="miniapp-card">
        <div className="miniapp-profile">
          <div>
            <strong className="miniapp-profile__name">Илья Андреев</strong>
            <span className="miniapp-profile__handle">@ilyaally</span>
          </div>
          <span className="miniapp-profile__id">#AL-48291</span>
        </div>
      </article>

      <article className="miniapp-card miniapp-card--row">
        <div>
          <strong className="miniapp-card__value">Тема</strong>
          <p className="miniapp-card__text">{theme === "dark" ? "Тёмная" : "Светлая"} версия интерфейса.</p>
        </div>
        <button type="button" className="miniapp-button miniapp-button--ghost" onClick={onToggleTheme}>
          Переключить
        </button>
      </article>

      <article className="miniapp-card miniapp-card--row">
        <div>
          <strong className="miniapp-card__value">Приватность и безопасность</strong>
          <p className="miniapp-card__text">
            Условия, конфиденциальность, управление аккаунтом и быстрый вход в поддержку.
          </p>
        </div>
        <button type="button" className="miniapp-button miniapp-button--ghost">
          Открыть
        </button>
      </article>
    </section>
  );
}
