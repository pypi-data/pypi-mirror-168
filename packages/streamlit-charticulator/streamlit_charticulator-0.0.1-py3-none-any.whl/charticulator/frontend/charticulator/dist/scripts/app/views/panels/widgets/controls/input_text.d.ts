import * as React from "react";
export interface InputTextProps {
    defaultValue?: string;
    placeholder?: string;
    onEnter?: (value: string) => boolean;
    onCancel?: () => void;
}
export declare class InputText extends React.Component<InputTextProps, Record<string, unknown>> {
    inputElement: HTMLInputElement;
    componentWillUpdate(newProps: InputTextProps): void;
    doEnter(): void;
    doCancel(): void;
    get value(): string;
    set value(v: string);
    render(): JSX.Element;
}
