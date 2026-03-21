import { useEffect, useState } from "react";

import { AppFrame, GlassPanel, PrimaryButton, SectionHeading, ThemeToggle } from "@allyvpn/ui-web";

import "./styles/website.scss";

const plans = [
  { name: "Базовый", price: "$0", note: "Для первого знакомства с AllyVPN", features: ["5 локаций", "1 устройство", "AES-256"] },
  { name: "Месячный", price: "$12", note: "Удобно для старта", features: ["40+ локаций", "5 устройств", "Приоритетная настройка"] },
  { name: "Премиум", price: "$99", note: "Лучший выбор на год", features: ["80+ локаций", "Неограниченные конфиги", "Быстрая поддержка"] },
];

const highlights = [
  {
    title: "Контроль без перегруза",
    description: "Telegram Mini App отвечает за кабинет и поддержку, а нативное приложение остается сфокусированным на защите и скорости.",
  },
  {
    title: "Единая визуальная система",
    description: "Сайт, Mini App и мобильный клиент делят одну типографику, отступы, градиенты и язык взаимодействия.",
  },
  {
    title: "Готово к росту",
    description: "Дизайн-система модульная, поддерживает темы и готова к платежам, billing, onboarding и будущим desktop-клиентам.",
  },
];

export function WebsiteApp() {
  const [theme, setTheme] = useState<"dark" | "light">("dark");

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  return (
    <AppFrame
      eyebrow="AllyVPN Website"
      title="Публичный сайт AllyVPN"
      description="Публичный сайт с сильной продуктовой подачей: понятные тарифы, доверие, поддержка и чистый путь в Telegram Mini App и нативное приложение."
      sidebar={
        <GlassPanel elevated>
          <div className="website-sidebar">
            <div className="website-sidebar__brand">
              <span className="website-sidebar__mark" />
              <strong>AllyVPN</strong>
            </div>
            <div className="website-sidebar__list">
              <div className="website-sidebar__metric">
                <span className="website-sidebar__value">2 темы</span>
                <span className="website-sidebar__label">Единая система</span>
              </div>
              <div className="website-sidebar__metric">
                <span className="website-sidebar__value">3 продукта</span>
                <span className="website-sidebar__label">Сайт, Mini App, Mobile</span>
              </div>
              <div className="website-sidebar__metric">
                <span className="website-sidebar__value">1 стиль</span>
                <span className="website-sidebar__label">Общий UX-язык</span>
              </div>
            </div>
            <ThemeToggle checked={theme === "dark"} label="Оформление" onChange={() => setTheme(theme === "dark" ? "light" : "dark")} />
          </div>
        </GlassPanel>
      }
    >
      <section className="website-hero-grid">
        <GlassPanel elevated>
          <div className="website-hero-card">
            <span className="website-hero-card__badge">Фундамент готов</span>
            <h2 className="website-hero-card__title">Премиальное позиционирование для серьезного VPN-продукта.</h2>
            <p className="website-hero-card__description">
              Сайт усиливает доверие, объясняет тарифы, переводит пользователя в Telegram и выступает чистым внешним лицом сервиса.
            </p>
            <div className="website-hero-card__actions">
              <PrimaryButton>Скачать приложение</PrimaryButton>
              <PrimaryButton variant="ghost">Открыть Mini App</PrimaryButton>
            </div>
          </div>
        </GlassPanel>

        <GlassPanel>
          <div className="website-showcase">
            <span className="website-showcase__status">Защита через продукт</span>
            <div className="website-showcase__surface">
              <h3 className="website-showcase__title">Маркетинг с продуктовым контекстом.</h3>
              <p className="website-showcase__copy">Тарифы, доверительные сигналы, поддержка и прямой вход в экосистему аккаунта.</p>
            </div>
          </div>
        </GlassPanel>
      </section>

      <section className="website-section">
        <SectionHeading
          title="Тарифы, готовые к росту от MVP до billing"
          description="Landing page уже подготовлен под провайдера оплаты, скидки, годовые предложения и будущие маркетинговые сценарии."
        />
        <div className="website-plan-grid">
          {plans.map((plan) => (
            <GlassPanel key={plan.name} elevated={plan.name === "Премиум"}>
              <article className="website-plan-card">
                <header className="website-plan-card__header">
                  <div>
                    <h3 className="website-plan-card__title">{plan.name}</h3>
                    <p className="website-plan-card__note">{plan.note}</p>
                  </div>
                  <strong className="website-plan-card__price">{plan.price}</strong>
                </header>
                <ul className="website-plan-card__features">
                  {plan.features.map((feature) => (
                    <li key={feature}>{feature}</li>
                  ))}
                </ul>
                <PrimaryButton wide>{plan.name === "Базовый" ? "Начать бесплатно" : "Выбрать тариф"}</PrimaryButton>
              </article>
            </GlassPanel>
          ))}
        </div>
      </section>

      <section className="website-section">
        <SectionHeading
          title="Почему сайт нужен даже при наличии Telegram"
          description="Telegram это точка входа в продукт, но не замена discoverability, доверительным сигналам, контенту и дистрибуции."
        />
        <div className="website-highlight-grid">
          {highlights.map((item) => (
            <GlassPanel key={item.title}>
              <article className="website-highlight-card">
                <h3 className="website-highlight-card__title">{item.title}</h3>
                <p className="website-highlight-card__description">{item.description}</p>
              </article>
            </GlassPanel>
          ))}
        </div>
      </section>
    </AppFrame>
  );
}
