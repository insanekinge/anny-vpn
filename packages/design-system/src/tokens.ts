export const allyColors = {
  white: "#ffffff",
  violetPrimary: "#7c4acc",
  violetSoft: "#b699e6",
  ink: "#0f0d12",
  plum: "#2a1c40",
} as const;

export const allyTypography = {
  displayFamily: "\"Sora\", \"Segoe UI\", sans-serif",
  bodyFamily: "\"Manrope\", \"Segoe UI\", sans-serif",
  weights: {
    regular: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
} as const;

export const allySpacing = {
  xs: 6,
  sm: 10,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
} as const;

export const allyRadius = {
  sm: 14,
  md: 20,
  lg: 28,
  pill: 999,
} as const;

export const allyShadows = {
  glow: "0 22px 80px rgba(124, 74, 204, 0.32)",
  surface: "0 20px 50px rgba(8, 7, 10, 0.32)",
  stroke: "0 0 0 1px rgba(182, 153, 230, 0.22)",
} as const;

export const allyMotion = {
  fast: "160ms ease",
  base: "240ms cubic-bezier(0.2, 0.8, 0.2, 1)",
  slow: "420ms cubic-bezier(0.2, 0.8, 0.2, 1)",
} as const;
