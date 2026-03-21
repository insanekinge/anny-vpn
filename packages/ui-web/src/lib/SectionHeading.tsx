import styles from "./SectionHeading.module.scss";

type SectionHeadingProps = {
  title: string;
  description?: string;
  align?: "left" | "center";
};

export function SectionHeading({ title, description, align = "left" }: SectionHeadingProps) {
  return (
    <header className={`${styles["section-heading"]} ${styles[`section-heading--${align}`]}`}>
      <h2 className={styles["section-heading__title"]}>{title}</h2>
      {description ? <p className={styles["section-heading__description"]}>{description}</p> : null}
    </header>
  );
}
