import styles from "./BottomTabs.module.scss";

export type BottomTabItem = {
  id: string;
  label: string;
};

type BottomTabsProps = {
  items: BottomTabItem[];
  activeId: string;
  onSelect: (id: string) => void;
};

export function BottomTabs({ items, activeId, onSelect }: BottomTabsProps) {
  return (
    <nav className={styles["bottom-tabs"]}>
      {items.map((item) => (
        <button
          key={item.id}
          type="button"
          className={`${styles["bottom-tabs__item"]} ${
            item.id === activeId ? styles["bottom-tabs__item--active"] : ""
          }`}
          onClick={() => onSelect(item.id)}
        >
          {item.label}
        </button>
      ))}
    </nav>
  );
}
