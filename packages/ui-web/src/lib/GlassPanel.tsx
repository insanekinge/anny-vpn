import type { PropsWithChildren } from "react";

import styles from "./GlassPanel.module.scss";

type GlassPanelProps = PropsWithChildren<{
  elevated?: boolean;
  compact?: boolean;
}>;

export function GlassPanel({ children, elevated = false, compact = false }: GlassPanelProps) {
  const className = [
    styles["glass-panel"],
    elevated ? styles["glass-panel--elevated"] : "",
    compact ? styles["glass-panel--compact"] : "",
  ]
    .filter(Boolean)
    .join(" ");

  return <section className={className}>{children}</section>;
}
