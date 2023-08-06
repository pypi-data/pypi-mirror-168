import * as React from "react";
interface ReorderStringsValueProps {
    items: string[];
    onConfirm: (items: string[], customOrder: boolean, sortOrder: boolean) => void;
    allowReset?: boolean;
    onReset?: () => string[];
}
interface ReorderStringsValueState {
    items: string[];
    customOrder: boolean;
    sortOrder: boolean;
}
export declare class ReorderStringsValue extends React.Component<ReorderStringsValueProps, ReorderStringsValueState> {
    state: ReorderStringsValueState;
    render(): JSX.Element;
}
export {};
