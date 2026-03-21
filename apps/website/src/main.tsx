import React from "react";
import ReactDOM from "react-dom/client";

import "@allyvpn/design-system/styles/fonts.css";
import "@allyvpn/design-system/styles/theme.css";

import { WebsiteApp } from "./WebsiteApp";
import "./styles/app.scss";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <WebsiteApp />
  </React.StrictMode>,
);
