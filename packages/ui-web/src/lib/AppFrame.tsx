import type { PropsWithChildren, ReactNode } from "react";

import styles from "./AppFrame.module.scss";

type AppFrameProps = PropsWithChildren<{
  eyebrow?: string;
  title: string;
  description?: string;
  sidebar?: ReactNode;
}>;

export function AppFrame({ children, eyebrow, title, description, sidebar }: AppFrameProps) {
  return (
    <div className={styles["app-frame"]}>
      <div className={styles["app-frame__backdrop"]} />
      <main className={styles["app-frame__layout"]}>
        <section className={styles["app-frame__content"]}>
          <header className={styles["app-frame__hero"]}>
            {eyebrow ? <span className={styles["app-frame__eyebrow"]}>{eyebrow}</span> : null}
            <h1 className={styles["app-frame__title"]}>{title}</h1>
            {description ? <p className={styles["app-frame__description"]}>{description}</p> : null}
          </header>
          {children}
        </section>
        {sidebar ? <aside className={styles["app-frame__sidebar"]}>{sidebar}</aside> : null}
      </main>
    </div>
  );
}
