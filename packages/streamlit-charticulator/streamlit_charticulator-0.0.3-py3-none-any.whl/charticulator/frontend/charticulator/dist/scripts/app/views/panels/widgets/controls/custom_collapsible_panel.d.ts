import { CSSProperties } from "react";
import { AppStore } from "../../../../../app/stores";
interface CollapsiblePanelProps {
    widgets: JSX.Element[];
    header?: string;
    styles?: CSSProperties;
    store?: AppStore;
}
export declare const CustomCollapsiblePanel: ({ widgets, header, styles, store, }: CollapsiblePanelProps) => JSX.Element;
interface PanelHeaderProps {
    header: string;
    collapsed: boolean;
    setCollapsed: (value: boolean) => void;
}
export declare const PanelHeader: ({ header, setCollapsed, collapsed, }: PanelHeaderProps) => JSX.Element;
export {};
