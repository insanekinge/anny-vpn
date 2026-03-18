(function () {
  var guideOpen = true;
  var toastTimer = null;
  var selectedLocation = "Нью-Йорк, Соединённые Штаты";

  function byId(id) {
    return document.getElementById(id);
  }

  function queryAll(selector) {
    return document.querySelectorAll(selector);
  }

  function readParams() {
    var search = window.location.search || "";

    if (search.indexOf("?") === 0) {
      search = search.slice(1);
    }

    var params = {};

    if (!search) {
      return params;
    }

    search.split("&").forEach(function (pair) {
      var parts = pair.split("=");
      var key = decodeURIComponent(parts[0] || "");
      var value = decodeURIComponent(parts[1] || "");

      if (key) {
        params[key] = value;
      }
    });

    return params;
  }

  function inferTabFromSection(section) {
    var value = (section || "").toLowerCase();

    if (!value) {
      return "";
    }

    if (
      value.indexOf("billing") !== -1 ||
      value.indexOf("settings") !== -1 ||
      value.indexOf("privacy") !== -1 ||
      value.indexOf("support") !== -1
    ) {
      return "profile";
    }

    if (value.indexOf("subscription") !== -1) {
      return "home";
    }

    if (value.indexOf("server") !== -1 || value.indexOf("access") !== -1) {
      return "access";
    }

    return "";
  }

  function normalizeTab(tab, section) {
    var value = (tab || inferTabFromSection(section) || "").toLowerCase();

    if (value === "plans" || value === "tariffs" || value === "billing") {
      return "profile";
    }

    if (value === "my-access" || value === "access" || value === "configs" || value === "servers") {
      return "access";
    }

    if (value === "settings" || value === "support" || value === "profile") {
      return "profile";
    }

    return "home";
  }

  function showToast(message) {
    var toast = byId("toast");

    if (!toast) {
      return;
    }

    if (toastTimer) {
      window.clearTimeout(toastTimer);
    }

    toast.textContent = message;
    toast.removeAttribute("hidden");
    toast.className = "toast toast--visible";

    toastTimer = window.setTimeout(function () {
      toast.className = "toast";
      toast.setAttribute("hidden", "hidden");
    }, 2200);
  }

  function setTheme(theme) {
    var toggle = byId("theme-toggle");
    var themeCopy = byId("theme-copy");

    document.documentElement.setAttribute("data-theme", theme);

    if (themeCopy) {
      themeCopy.textContent = theme === "dark" ? "Dark mode" : "Light mode";
    }

    if (toggle) {
      toggle.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
      toggle.className = theme === "dark" ? "toggle toggle--active" : "toggle";
    }

    try {
      if (window.Telegram && window.Telegram.WebApp) {
        var webApp = window.Telegram.WebApp;
        if (webApp.setHeaderColor) {
          webApp.setHeaderColor(theme === "dark" ? "#0f0d12" : "#ffffff");
        }
        if (webApp.setBackgroundColor) {
          webApp.setBackgroundColor(theme === "dark" ? "#0f0d12" : "#f4f1fa");
        }
      }
    } catch (error) {
      if (window.console && window.console.warn) {
        window.console.warn("Theme bridge failed", error);
      }
    }
  }

  function activateTab(tabId, sectionId) {
    var normalized = normalizeTab(tabId, sectionId);
    var tabs = queryAll("[data-tab]");
    var screens = queryAll("[data-screen]");
    var index;

    for (index = 0; index < tabs.length; index += 1) {
      if (tabs[index].getAttribute("data-tab") === normalized) {
        tabs[index].className = "tabbar__item tabbar__item--active";
        tabs[index].setAttribute("aria-current", "page");
      } else {
        tabs[index].className = "tabbar__item";
        tabs[index].removeAttribute("aria-current");
      }
    }

    for (index = 0; index < screens.length; index += 1) {
      if (screens[index].getAttribute("data-screen") === normalized) {
        screens[index].removeAttribute("hidden");
      } else {
        screens[index].setAttribute("hidden", "hidden");
      }
    }

    if (sectionId) {
      window.setTimeout(function () {
        var element = byId(sectionId);
        if (element && element.scrollIntoView) {
          element.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      }, 50);
    } else {
      window.scrollTo(0, 0);
    }
  }

  function updateHomeLocation() {
    var statusCopy = byId("subscription-status-copy");

    if (statusCopy) {
      statusCopy.textContent = "Активна • " + selectedLocation;
    }
  }

  function toggleGuide() {
    var guide = byId("guide-card");
    guideOpen = !guideOpen;

    if (!guide) {
      return;
    }

    if (guideOpen) {
      guide.removeAttribute("hidden");
      showToast("Инструкция открыта");
    } else {
      guide.setAttribute("hidden", "hidden");
      showToast("Инструкция скрыта");
    }
  }

  function refreshServers() {
    var stamp = byId("refresh-status");

    if (stamp) {
      stamp.textContent = "Updated just now";
    }

    showToast("Список серверов обновлён");
  }

  function activateServer(card) {
    var cards = queryAll(".server-card");
    var index;

    for (index = 0; index < cards.length; index += 1) {
      if (cards[index] === card) {
        cards[index].className = "server-card server-card--active";
      } else {
        cards[index].className = "server-card";
      }
    }

    selectedLocation = card.getAttribute("data-location") || selectedLocation;
    updateHomeLocation();
    showToast("Выбран сервер: " + (card.getAttribute("data-server-name") || "локация"));
  }

  function filterServers(value) {
    var text = (value || "").toLowerCase();
    var cards = queryAll(".server-card");
    var groups = queryAll(".server-group");
    var index;

    for (index = 0; index < cards.length; index += 1) {
      var name = cards[index].getAttribute("data-server-name") || "";
      var location = cards[index].getAttribute("data-location") || "";
      var haystack = (name + " " + location).toLowerCase();

      if (!text || haystack.indexOf(text) !== -1) {
        cards[index].removeAttribute("hidden");
      } else {
        cards[index].setAttribute("hidden", "hidden");
      }
    }

    for (index = 0; index < groups.length; index += 1) {
      var visibleCards = groups[index].querySelectorAll(".server-card:not([hidden])");

      if (visibleCards.length) {
        groups[index].removeAttribute("hidden");
      } else {
        groups[index].setAttribute("hidden", "hidden");
      }
    }
  }

  function bootstrapTelegram() {
    try {
      if (!window.Telegram || !window.Telegram.WebApp) {
        setTheme("dark");
        return;
      }

      var webApp = window.Telegram.WebApp;
      var theme = webApp.colorScheme === "light" ? "light" : "dark";

      webApp.ready();
      webApp.expand();
      setTheme(theme);
    } catch (error) {
      setTheme("dark");
      if (window.console && window.console.warn) {
        window.console.warn("Telegram bootstrap failed", error);
      }
    }
  }

  function handleAction(action) {
    if (action === "billing-view") {
      showToast("История платежей появится на следующем этапе");
      return true;
    }

    if (action === "privacy-open") {
      showToast("Раздел приватности будет расширен позже");
      return true;
    }

    if (action === "support-open") {
      showToast("Тестовый переход в поддержку выполнен");
      return true;
    }

    return false;
  }

  function findActionTarget(start) {
    var target = start;

    while (target && target !== document.body) {
      if (target.getAttribute && target.getAttribute("data-tab")) {
        return { type: "tab", value: target.getAttribute("data-tab") };
      }

      if (target.getAttribute && target.getAttribute("data-target-tab")) {
        return {
          type: "target-tab",
          value: target.getAttribute("data-target-tab"),
          section: target.getAttribute("data-target-section") || ""
        };
      }

      if (target.getAttribute && target.getAttribute("data-action")) {
        return { type: "action", value: target.getAttribute("data-action") };
      }

      if (target.id === "refresh-servers") {
        return { type: "refresh" };
      }

      if (target.id === "guide-toggle") {
        return { type: "guide" };
      }

      if (target.id === "theme-toggle") {
        return { type: "theme" };
      }

      if (target.className && String(target.className).indexOf("server-card") !== -1) {
        return { type: "server", node: target };
      }

      target = target.parentNode;
    }

    return null;
  }

  function handleClick(event) {
    var action = findActionTarget(event.target);

    if (!action) {
      return;
    }

    if (action.type === "tab") {
      activateTab(action.value);
      return;
    }

    if (action.type === "target-tab") {
      activateTab(action.value, action.section);
      return;
    }

    if (action.type === "refresh") {
      refreshServers();
      return;
    }

    if (action.type === "guide") {
      toggleGuide();
      return;
    }

    if (action.type === "theme") {
      var current = document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
      setTheme(current === "dark" ? "light" : "dark");
      showToast(current === "dark" ? "Включена светлая тема" : "Включена тёмная тема");
      return;
    }

    if (action.type === "server") {
      activateServer(action.node);
      return;
    }

    if (action.type === "action") {
      handleAction(action.value);
    }
  }

  function handleInput(event) {
    if (event.target && event.target.id === "server-search") {
      filterServers(event.target.value);
    }
  }

  function start() {
    document.addEventListener("click", handleClick, false);
    document.addEventListener("input", handleInput, false);
    bootstrapTelegram();
    updateHomeLocation();

    var params = readParams();
    activateTab(params.tab || "", params.section || "");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
