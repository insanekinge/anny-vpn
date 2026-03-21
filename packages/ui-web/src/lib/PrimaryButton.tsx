import type { ButtonHTMLAttributes, PropsWithChildren } from "react";

import styles from "./PrimaryButton.module.scss";

type PrimaryButtonProps = PropsWithChildren<
  ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?: "primary" | "ghost";
    wide?: boolean;
  }
>;

export function PrimaryButton({
  children,
  className,
  variant = "primary",
  wide = false,
  ...props
}: PrimaryButtonProps) {
  const computedClassName = [
    styles["primary-button"],
    styles[`primary-button--${variant}`],
    wide ? styles["primary-button--wide"] : "",
    className ?? "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <button {...props} className={computedClassName}>
      {children}
    </button>
  );
}
