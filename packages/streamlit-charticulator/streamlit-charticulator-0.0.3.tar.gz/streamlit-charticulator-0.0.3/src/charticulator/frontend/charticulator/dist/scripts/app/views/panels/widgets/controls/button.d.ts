import * as React from "react";
export interface ButtonProps {
    icon?: string;
    text?: string;
    title?: string;
    active?: boolean;
    disabled?: boolean;
    onClick?: () => void;
}
export declare class Button extends React.Component<ButtonProps, Record<string, unknown>> {
    render(): JSX.Element;
}
export interface UpdownButtonProps {
    onClick: (part: "up" | "down") => void;
}
export declare function UpdownButton(props: UpdownButtonProps): JSX.Element;
export interface CheckBoxProps {
    value: boolean;
    text?: string;
    title?: string;
    fillWidth?: boolean;
    onChange?: (newValue: boolean) => void;
}
export declare class CheckBox extends React.Component<CheckBoxProps, Record<string, unknown>> {
    render(): JSX.Element;
}
