import styles from "./ThemeToggle.module.scss";

type ThemeToggleProps = {
  checked: boolean;
  label: string;
  onChange: () => void;
  checkedHint?: string;
  uncheckedHint?: string;
};

export function ThemeToggle({
  checked,
  label,
  onChange,
  checkedHint = "Темная тема",
  uncheckedHint = "Светлая тема",
}: ThemeToggleProps) {
  return (
    <button className={styles["theme-toggle"]} onClick={onChange} type="button" aria-pressed={checked}>
      <span className={styles["theme-toggle__content"]}>
        <span className={styles["theme-toggle__label"]}>{label}</span>
        <span className={styles["theme-toggle__hint"]}>{checked ? checkedHint : uncheckedHint}</span>
      </span>
      <span
        className={`${styles["theme-toggle__track"]} ${
          checked ? styles["theme-toggle__track--checked"] : ""
        }`}
      >
        <span className={styles["theme-toggle__thumb"]} />
      </span>
    </button>
  );
}
