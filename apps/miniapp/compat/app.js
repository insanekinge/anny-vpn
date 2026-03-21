(function () {
  var state = {
    user_name: "Илья Андреев",
    user_short_name: "Илья",
    user_handle: "@ilyaally",
    account_id: "#AL-48291",
    member_since: "Март 2025",
    status: "active",
    status_badge: "Активна",
    hero_helper: "Ваш VPN готов к использованию",
    plan_name: "Стандарт",
    plan_price: "300 ₽ / месяц",
    expires_at: "15 июня 2026",
    days_left_copy: "Осталось 87 дней подписки",
    renew_copy: "Тариф «Стандарт» активен. Продлите доступ заранее или перейдите на Plus для максимальной скорости.",
    marzban_username: "user_469102712",
    traffic_used: "45.2",
    traffic_total: "100",
    recommended_title: "AllyVPN VLESS",
    recommended_reason: "Оптимальный баланс скорости и стабильности. Работает в большинстве сетей и остаётся рекомендуемым протоколом по умолчанию.",
    subscription_url: "https://sub.allyvpn.com/api/v1/client/subscribe?token=a1ly-vpn-portal-secure-token",
    recommended_config: "vless://user_469102712@allyvpn.com:443?security=tls&type=ws&path=%2Fvpn&host=allyvpn.com#AllyVPN-VLESS",
    vmess_config: "vmess://eyJhZGQiOiJhbGx5dnBuLmNvbSIsInBvcnQiOiI0NDMiLCJpZCI6ImFsbHktdXNlci0xMjMiLCJhaWQiOiIwIn0=",
    trojan_config: "trojan://password123@server.allyvpn.com:443?security=tls#AllyVPN-Trojan",
    shadowsocks_config: "ss://YWVzLTI1Ni1nY206cGFzc0BhbGx5dnBuLmNvbTo4NDQz#AllyVPN-SS"
  };

  var guideMessages = {
    hiddify: "Открыта инструкция для Hiddify.",
    v2rayng: "Открыта инструкция для v2rayNG.",
    streisand: "Открыта инструкция для Streisand.",
    nekoray: "Открыта инструкция для Nekoray."
  };

  var toastTimer = null;

  function byId(id) {
    return document.getElementById(id);
  }

  function queryAll(selector) {
    return document.querySelectorAll(selector);
  }

  function readParams() {
    var raw = window.location.search ? window.location.search.replace(/^\?/, "") : "";
    var params = {};
    if (!raw) return params;

    raw.split("&").forEach(function (pair) {
      var parts = pair.split("=");
      var key = decodeURIComponent(parts[0] || "");
      var value = decodeURIComponent(parts.slice(1).join("=") || "");
      if (key) params[key] = value;
    });

    return params;
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function preview(text) {
    return text.length > 58 ? text.slice(0, 58) + "..." : text;
  }

  function bind(name, value) {
    queryAll('[data-bind="' + name + '"]').forEach(function (node) {
      node.textContent = value;
    });
  }

  function updateUsage() {
    var used = parseFloat(state.traffic_used);
    var total = parseFloat(state.traffic_total);
    var width = total > 0 ? clamp((used / total) * 100, 0, 100) : 0;

    [byId("desktop-usage-bar"), byId("mobile-usage-bar")].forEach(function (bar) {
      if (bar) bar.style.width = width + "%";
    });
  }

  function applyStatus(status) {
    state.status = status;

    if (status === "soon") {
      state.status_badge = "Истекает скоро";
      state.hero_helper = "Доступ скоро завершится. Продлите подписку заранее, чтобы не потерять подключение.";
    } else if (status === "expired") {
      state.status_badge = "Истекла";
      state.hero_helper = "Подписка завершилась. Продлите тариф, чтобы снова получить доступ к конфигам.";
    } else if (status === "error") {
      state.status_badge = "Ошибка";
      state.hero_helper = "Возникла проблема с доступом. Проверьте диагностику или напишите в поддержку.";
    } else {
      state.status_badge = "Активна";
      state.hero_helper = "Ваш VPN готов к использованию";
    }

    var warning = byId("desktop-warning");
    if (warning) warning.hidden = status !== "soon";
  }

  function render() {
    state.subscription_url_preview = preview(state.subscription_url);
    state.recommended_config_preview = preview(state.recommended_config);
    state.alt_vmess_preview = preview(state.vmess_config);
    state.alt_trojan_preview = preview(state.trojan_config);

    Object.keys(state).forEach(function (key) {
      bind(key, state[key]);
    });

    updateUsage();
  }

  function showToast(message) {
    var toast = byId("toast");
    if (!toast) return;

    if (toastTimer) {
      window.clearTimeout(toastTimer);
    }

    toast.hidden = false;
    toast.textContent = message;

    toastTimer = window.setTimeout(function () {
      toast.hidden = true;
    }, 2200);
  }

  function copyValue(name) {
    var value = state[name];
    if (!value) return;

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(value).then(
        function () {
          showToast("Скопировано");
        },
        function () {
          showToast("Не удалось скопировать");
        }
      );
      return;
    }

    showToast("Буфер обмена недоступен");
  }

  function setTheme(theme) {
    var themeCopy = theme === "light" ? "Светлая тема включена" : "Тёмная тема включена";

    document.documentElement.setAttribute("data-theme", theme);

    queryAll("[data-theme-copy]").forEach(function (node) {
      node.textContent = themeCopy;
    });

    queryAll("[data-theme-toggle]").forEach(function (node) {
      node.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
    });

    try {
      if (window.Telegram && window.Telegram.WebApp) {
        var webApp = window.Telegram.WebApp;
        if (webApp.setHeaderColor) webApp.setHeaderColor(theme === "dark" ? "#0b0912" : "#ffffff");
        if (webApp.setBackgroundColor) webApp.setBackgroundColor(theme === "dark" ? "#0b0912" : "#f5f1fb");
      }
    } catch (error) {
      if (window.console) window.console.warn(error);
    }
  }

  function openReveal(name) {
    var modal = byId("reveal-modal");
    var title = byId("reveal-title");
    var content = byId("reveal-content");
    var copy = byId("reveal-copy");
    var labels = {
      subscription_url: "Subscription URL",
      recommended_config: "Рекомендуемый конфиг"
    };

    if (!modal || !title || !content || !copy) return;

    modal.hidden = false;
    title.textContent = labels[name] || "Данные";
    content.textContent = state[name] || "";
    copy.setAttribute("data-copy", name);
  }

  function closeReveal() {
    var modal = byId("reveal-modal");
    if (modal) modal.hidden = true;
  }

  function setMobileTab(tab) {
    queryAll(".mobile-tabbar__item").forEach(function (node) {
      node.className =
        node.getAttribute("data-tab") === tab
          ? "mobile-tabbar__item mobile-tabbar__item--active"
          : "mobile-tabbar__item";
    });

    queryAll(".mobile-app .screen").forEach(function (node) {
      node.hidden = node.getAttribute("data-screen") !== tab;
    });

    window.scrollTo(0, 0);
  }

  function normalizeDesktopSection(section) {
    if (section === "overview") return "home";
    if (section === "connection" || section === "guides") return "access";
    if (section === "profile") return "profile";
    return section || "home";
  }

  function setDesktopSection(section, shouldScroll) {
    var normalized = normalizeDesktopSection(section);

    queryAll(".desktop-section-nav__item").forEach(function (node) {
      node.className =
        node.getAttribute("data-desktop-section") === normalized
          ? "desktop-section-nav__item desktop-section-nav__item--active"
          : "desktop-section-nav__item";
    });

    queryAll(".desktop-page").forEach(function (node) {
      node.hidden = node.getAttribute("data-desktop-anchor") !== normalized;
    });

    if (shouldScroll) {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }

  function stripDesktopAnchor(node) {
    if (!node) return;

    node.classList.remove("desktop-anchor");
    node.removeAttribute("data-desktop-anchor");

    if ((node.getAttribute("id") || "").indexOf("desktop-") === 0) {
      node.removeAttribute("id");
    }
  }

  function createDesktopStack() {
    var stack = document.createElement("div");
    stack.className = "desktop-stack";
    return stack;
  }

  function createDesktopSection(anchor, title, subtitle, extraClass) {
    var section = document.createElement("section");
    var head = document.createElement("div");
    var heading = document.createElement("h2");
    var copy = document.createElement("p");
    var grid = document.createElement("div");

    section.className = "desktop-section desktop-anchor" + (extraClass ? " " + extraClass : "");
    section.id = "desktop-" + anchor;
    section.setAttribute("data-desktop-anchor", anchor);

    head.className = "desktop-section__head";
    heading.className = "section-title";
    heading.textContent = title;
    copy.className = "desktop-section__subtitle";
    copy.textContent = subtitle;
    head.appendChild(heading);
    head.appendChild(copy);

    grid.className = "desktop-section__grid";
    section.appendChild(head);
    section.appendChild(grid);

    return {
      section: section,
      grid: grid
    };
  }

  function createActionCard(actionGrid) {
    if (!actionGrid) return null;

    var card = document.createElement("article");
    var head = document.createElement("div");
    var title = document.createElement("h3");
    var copy = document.createElement("p");

    card.className = "card action-card";
    head.className = "desktop-section__head desktop-section__head--compact";
    title.className = "section-title section-title--compact";
    title.textContent = "Быстрые действия";
    copy.className = "desktop-section__subtitle";
    copy.textContent = "Основные сценарии собраны в одном месте: подключение, копирование ссылки, продление и поддержка.";

    head.appendChild(title);
    head.appendChild(copy);
    card.appendChild(head);
    card.appendChild(actionGrid);

    return card;
  }

  function createGuideGrid(source) {
    var grid = document.createElement("div");

    if (!source) return null;

    grid.className = "desktop-guide-grid";
    Array.prototype.forEach.call(source.querySelectorAll(".guide"), function (guideCard) {
      grid.appendChild(guideCard);
    });

    return grid;
  }

  function buildDesktopSections() {
    var portal = document.querySelector(".desktop-portal");
    var main;
    var side;
    var hero;
    var actionGrid;
    var recommend;
    var details;
    var protoBlock;
    var quickCard;
    var billingCard;
    var infoCard;
    var guidesSection;
    var diagSection;
    var renewCard;
    var accountCard;
    var home;
    var access;
    var profile;
    var homeLeft;
    var homeRight;
    var accessLeft;
    var accessRight;
    var profileLeft;
    var profileRight;
    var actionCard;
    var guideGrid;

    if (!portal || portal.getAttribute("data-layout-built") === "true") return;
    if (!window.matchMedia || !window.matchMedia("(min-width: 1024px)").matches) return;

    main = portal.querySelector(".desktop-main");
    side = portal.querySelector(".desktop-side");

    if (!main || !side) return;

    hero = main.querySelector(".hero-card");
    actionGrid = main.querySelector(".action-grid");
    recommend = main.querySelector(".recommend-card");
    details = main.querySelector(".recommend-card + article.card");
    protoBlock = main.querySelector(".proto-block");

    quickCard = side.querySelector(".quick-card");
    billingCard = side.querySelector(".billing-card");
    infoCard = side.querySelector(".info-card");
    guidesSection = side.querySelector(".side-list--guides");
    diagSection = side.querySelector(".side-list--diag");
    renewCard = side.querySelector(".renew");
    accountCard = side.querySelector(".account");

    if (!hero || !recommend || !details || !protoBlock || !quickCard || !billingCard || !guidesSection || !accountCard) {
      return;
    }

    [hero, recommend, guidesSection, accountCard].forEach(stripDesktopAnchor);

    home = createDesktopSection(
      "home",
      "Главная",
      "Сводка по аккаунту, статусу подписки и ключевым действиям — так же, как в мобильной версии.",
      "desktop-section--home"
    );
    access = createDesktopSection(
      "access",
      "Доступ",
      "Подключение, импорт, конфиги, протоколы и инструкции собраны на одной desktop-странице."
    );
    profile = createDesktopSection(
      "profile",
      "Профиль и биллинг",
      "Аккаунт и тарифы сгруппированы отдельно от технических блоков подключения.",
      "desktop-section--profile"
    );

    home.grid.className += " desktop-section__grid--overview";
    access.grid.className += " desktop-section__grid--access";
    profile.grid.className += " desktop-section__grid--profile";

    homeLeft = createDesktopStack();
    homeRight = createDesktopStack();
    accessLeft = createDesktopStack();
    accessRight = createDesktopStack();
    profileLeft = createDesktopStack();
    profileRight = createDesktopStack();

    queryAll(".desktop-section-nav__item").forEach(function (node) {
      var type = node.getAttribute("data-desktop-section");
      if (type === "overview") {
        node.setAttribute("data-desktop-section", "home");
        node.textContent = "Главная";
      } else if (type === "connection" || type === "guides") {
        node.setAttribute("data-desktop-section", "access");
        node.textContent = "Доступ";
      } else if (type === "profile") {
        node.setAttribute("data-desktop-section", "profile");
        node.textContent = "Профиль";
      }
    });

    if (queryAll(".desktop-section-nav__item")[0]) {
      queryAll(".desktop-section-nav__item")[0].setAttribute("data-desktop-section", "home");
      queryAll(".desktop-section-nav__item")[0].textContent = "Главная";
    }
    if (queryAll(".desktop-section-nav__item")[1]) {
      queryAll(".desktop-section-nav__item")[1].setAttribute("data-desktop-section", "access");
      queryAll(".desktop-section-nav__item")[1].textContent = "Доступ";
    }
    if (queryAll(".desktop-section-nav__item")[2]) {
      queryAll(".desktop-section-nav__item")[2].remove();
    }
    if (queryAll(".desktop-section-nav__item")[2]) {
      queryAll(".desktop-section-nav__item")[2].setAttribute("data-desktop-section", "profile");
      queryAll(".desktop-section-nav__item")[2].textContent = "Профиль";
    }

    actionCard = createActionCard(actionGrid);
    if (actionCard) homeLeft.appendChild(actionCard);

    homeLeft.insertBefore(hero, homeLeft.firstChild);
    if (diagSection) homeRight.appendChild(diagSection);
    if (renewCard) homeRight.appendChild(renewCard);
    home.grid.appendChild(homeLeft);
    home.grid.appendChild(homeRight);

    accessLeft.appendChild(recommend);
    accessLeft.appendChild(details);
    if (protoBlock) accessLeft.appendChild(protoBlock);
    if (quickCard) accessRight.appendChild(quickCard);
    if (infoCard) accessRight.appendChild(infoCard);
    guideGrid = createGuideGrid(guidesSection);
    if (guideGrid) accessRight.appendChild(guideGrid);
    access.grid.appendChild(accessLeft);
    access.grid.appendChild(accessRight);

    profileLeft.appendChild(accountCard);
    profileRight.appendChild(billingCard);
    profile.grid.appendChild(profileLeft);
    profile.grid.appendChild(profileRight);

    portal.innerHTML = "";
    home.section.className += " desktop-page";
    access.section.className += " desktop-page";
    profile.section.className += " desktop-page";
    portal.appendChild(home.section);
    portal.appendChild(access.section);
    portal.appendChild(profile.section);
    portal.setAttribute("data-layout-built", "true");
  }

  function toggleAccordion(targetId, toggle) {
    var panel = byId(targetId);
    if (!panel) return;

    var expanded = !panel.hidden;
    panel.hidden = expanded;

    if (toggle) {
      toggle.setAttribute("aria-expanded", expanded ? "false" : "true");
    }
  }

  function recommendedApp() {
    var ua = navigator.userAgent || "";

    if (/Android/i.test(ua)) {
      return {
        name: "Hiddify",
        guide: "hiddify",
        copy: "На Android удобнее всего импортировать ссылку подписки через Hiddify и сразу использовать VLESS."
      };
    }

    if (/iPhone|iPad|iPod/i.test(ua)) {
      return {
        name: "Streisand",
        guide: "streisand",
        copy: "Для iPhone и iPad рекомендуем Streisand: он быстро импортирует подписку и стабильно работает с VLESS."
      };
    }

    if (/Windows/i.test(ua)) {
      return {
        name: "Nekoray",
        guide: "nekoray",
        copy: "На Windows проще всего подключиться через Nekoray и импорт по ссылке подписки."
      };
    }

    return {
      name: "Hiddify",
      guide: "hiddify",
      copy: "Для большинства устройств лучше всего подойдёт Hiddify: быстрый импорт, стабильный VLESS и понятный интерфейс."
    };
  }

  function handleAction(action) {
    var messages = {
      connect: "Тестовый сценарий подключения запущен. Здесь будет интеграция с приложением и VPS.",
      "connect-recommended": "Открываем рекомендуемое подключение через AllyVPN VLESS.",
      renew: "Откроется сценарий продления тарифа или перехода на Plus.",
      support: "Откроется поддержка AllyVPN.",
      billing: "Раздел биллинга подготовлен. На следующем этапе здесь появятся реальные способы оплаты.",
      privacy: "Откроется раздел приватности и безопасности.",
      legal: "Откроются условия использования и политика конфиденциальности.",
      signout: "Выполняется выход из аккаунта.",
      "open-guide": "Открываем общую инструкцию по подключению."
    };

    showToast(messages[action] || "Тестовое действие выполнено");
  }

  function bootstrapTelegram(theme) {
    try {
      if (!window.Telegram || !window.Telegram.WebApp) {
        setTheme(theme || "dark");
        return;
      }

      var webApp = window.Telegram.WebApp;
      webApp.ready();
      webApp.expand();
      setTheme(theme || (webApp.colorScheme === "light" ? "light" : "dark"));
    } catch (error) {
      setTheme(theme || "dark");
    }
  }

  function onClick(event) {
    var target = event.target;

    while (target && target !== document.body) {
      if (target.hasAttribute("data-tab")) {
        setMobileTab(target.getAttribute("data-tab"));
        return;
      }

      if (target.hasAttribute("data-target-tab")) {
        setMobileTab(target.getAttribute("data-target-tab"));
        return;
      }

      if (target.hasAttribute("data-desktop-section")) {
        setDesktopSection(target.getAttribute("data-desktop-section"), true);
        return;
      }

      if (target.hasAttribute("data-copy")) {
        copyValue(target.getAttribute("data-copy"));
        return;
      }

      if (target.hasAttribute("data-reveal")) {
        openReveal(target.getAttribute("data-reveal"));
        return;
      }

      if (target.hasAttribute("data-theme-toggle")) {
        var nextTheme = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
        setTheme(nextTheme);
        showToast(nextTheme === "light" ? "Включена светлая тема" : "Включена тёмная тема");
        return;
      }

      if (target.hasAttribute("data-action")) {
        handleAction(target.getAttribute("data-action"));
        return;
      }

      if (target.hasAttribute("data-guide")) {
        showToast(guideMessages[target.getAttribute("data-guide")] || "Открыта инструкция");
        return;
      }

      if (target.hasAttribute("data-accordion-target")) {
        toggleAccordion(target.getAttribute("data-accordion-target"), target);
        return;
      }

      if (target.hasAttribute("data-close-modal")) {
        closeReveal();
        return;
      }

      target = target.parentNode;
    }
  }

  function init() {
    var params = readParams();

    if (params.status) applyStatus(params.status);
    if (params.used) state.traffic_used = params.used;
    if (params.total) state.traffic_total = params.total;
    if (params.user) state.user_name = params.user;
    if (params.handle) state.user_handle = params.handle;

    var app = recommendedApp();
    var appName = byId("desktop-app-name");
    var appCopy = byId("desktop-app-copy");
    var openGuide = byId("desktop-open-guide");

    if (appName) appName.textContent = app.name;
    if (appCopy) appCopy.textContent = app.copy;
    if (openGuide) openGuide.setAttribute("data-guide", app.guide);

    buildDesktopSections();
    render();
    bootstrapTelegram(params.theme === "light" ? "light" : "dark");
    document.addEventListener("click", onClick, false);
    setMobileTab(params.tab || "home");
    setDesktopSection(params.section || "home", false);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
