import * as React from "react";
import { DataType } from "../../../../../core/specification";
interface ReorderStringsValueProps {
    items: string[];
    onConfirm: (items: string[], customOrder: boolean, sortOrder: boolean) => void;
    sortedCategories?: string[];
    allowReset?: boolean;
    onReset?: () => string[];
    itemsDataType?: DataType.Number | DataType.String;
    allowDragItems?: boolean;
    onReorderHandler?: () => void;
    onButtonHandler?: () => void;
}
interface ReorderStringsValueState {
    items: string[];
    customOrder: boolean;
    sortOrder: boolean;
}
export declare class FluentUIReorderStringsValue extends React.Component<ReorderStringsValueProps, ReorderStringsValueState> {
    state: ReorderStringsValueState;
    render(): JSX.Element;
}
export {};
