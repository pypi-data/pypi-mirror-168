import * as React from "react";
import { LabelPosition } from "../../../../../core/prototypes/controls";
import { PopupContext } from "../../../../controllers/popup_controller";
export declare function DropdownListView(props: {
    list: {
        name: string;
        url?: string;
        text?: string;
        font?: string;
    }[];
    onClick?: (name: string) => void;
    onClose?: () => void;
    selected?: string;
    context: PopupContext;
}): JSX.Element;
export interface SelectProps {
    icons?: string[];
    options: string[];
    labels?: string[];
    showText?: boolean;
    labelPosition?: LabelPosition;
    tooltip?: string;
    value: string;
    onChange: (active: string) => void;
}
export declare class Select extends React.Component<SelectProps, {
    active: boolean;
}> {
    constructor(props: SelectProps);
    private startDropdown;
    private _startDropdown;
    private anchor;
    render(): JSX.Element;
}
export declare class Radio extends React.Component<SelectProps, Record<string, unknown>> {
    render(): JSX.Element;
}
