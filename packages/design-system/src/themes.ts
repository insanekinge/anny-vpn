import { allyColors } from "./tokens";

export const allyThemes = {
  dark: {
    id: "dark",
    background: allyColors.ink,
    surface: "#17141c",
    surfaceMuted: "#1f1b27",
    border: "rgba(182, 153, 230, 0.18)",
    text: allyColors.white,
    textMuted: "#b9b1c7",
    accent: allyColors.violetPrimary,
    accentSoft: allyColors.violetSoft,
    accentDeep: allyColors.plum,
    success: "#27d17f",
    warning: "#ffbf47",
  },
  light: {
    id: "light",
    background: "#f7f5fb",
    surface: allyColors.white,
    surfaceMuted: "#efe9fa",
    border: "rgba(42, 28, 64, 0.12)",
    text: allyColors.ink,
    textMuted: "#63577a",
    accent: allyColors.violetPrimary,
    accentSoft: allyColors.violetSoft,
    accentDeep: allyColors.plum,
    success: "#14b86f",
    warning: "#f1a907",
  },
} as const;

export type AllyThemeName = keyof typeof allyThemes;
