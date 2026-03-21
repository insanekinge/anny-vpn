import React from "react";
import ReactDOM from "react-dom/client";

import "@allyvpn/design-system/styles/fonts.css";
import "@allyvpn/design-system/styles/theme.css";

import { MiniApp } from "./MiniApp";
import "./styles/miniapp.scss";

const rootElement = document.getElementById("root");

if (!rootElement) {
  throw new Error("Mini App root container was not found.");
}

window.addEventListener("error", (event) => {
  rootElement.innerHTML = `
    <div style="min-height:100vh;padding:24px;background:#0f0d12;color:#ffffff;font-family:Segoe UI,sans-serif;">
      <h1 style="margin:0 0 12px;">AllyVPN Mini</h1>
      <p style="margin:0 0 8px;color:#b699e6;">Интерфейс не удалось запустить.</p>
      <pre style="white-space:pre-wrap;color:#ffffff;background:#17141c;padding:16px;border-radius:16px;border:1px solid rgba(182,153,230,.18);">${String(
        event.error?.message ?? event.message ?? "Unknown error",
      )}</pre>
    </div>
  `;
});

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <MiniApp />
  </React.StrictMode>,
);
