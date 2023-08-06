import * as React from "react";
import { Color, ColorGradient } from "../../../../../core";
import { AppStore } from "../../../../stores";
export interface InputColorProps {
    defaultValue: Color;
    allowNull?: boolean;
    label?: string;
    onEnter: (value: Color) => boolean;
    store?: AppStore;
    noDefaultMargin?: boolean;
    labelKey?: string;
    width?: number;
    underline?: boolean;
    stopPropagation?: boolean;
    pickerBeforeTextField?: boolean;
    styles?: {
        marginTop?: string;
    };
}
interface FluentInputColorState {
    open: boolean;
    color: string;
    value: string;
}
export declare class FluentInputColor extends React.Component<InputColorProps, FluentInputColorState> {
    constructor(props: InputColorProps);
    componentWillReceiveProps(nextProps: Readonly<InputColorProps>): void;
    private renderPicker;
    private renderEmptyColorPicker;
    render(): JSX.Element;
}
export interface InputColorGradientProps {
    defaultValue: ColorGradient;
    onEnter: (value: ColorGradient) => boolean;
}
export declare class InputColorGradient extends React.Component<InputColorGradientProps, Record<string, unknown>> {
    render(): JSX.Element;
}
export {};
