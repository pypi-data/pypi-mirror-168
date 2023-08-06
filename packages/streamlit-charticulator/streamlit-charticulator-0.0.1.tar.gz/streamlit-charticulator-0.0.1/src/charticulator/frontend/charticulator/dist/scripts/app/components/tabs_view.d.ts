import * as React from "react";
export interface TabsViewProps {
    tabs: {
        name: string;
        label: string;
        icon?: string;
    }[];
    currentTab: string;
    onSelect: (tabName: string) => void;
}
export declare class TabsView extends React.Component<TabsViewProps, Record<string, unknown>> {
    render(): JSX.Element;
}
