import { IGroupHeaderProps, IRenderFunction } from "@fluentui/react";
import * as React from "react";
import { AppStore } from "../../../../../app/stores";
interface CollapsiblePanelProps {
    header: string | IRenderFunction<IGroupHeaderProps>;
    widgets: JSX.Element[];
    isCollapsed?: boolean;
    alignVertically?: boolean;
    store?: AppStore;
}
export declare const CollapsiblePanel: React.FunctionComponent<CollapsiblePanelProps>;
export {};
