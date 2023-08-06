import * as React from "react";
import { ColorGradient } from "../../core";
export interface GradientPickerProps {
    defaultValue?: ColorGradient;
    onPick?: (gradient: ColorGradient) => void;
}
export interface GradientPickerState {
    currentTab: string;
    currentGradient: ColorGradient;
}
export declare enum Colorspace {
    LAB = "lab",
    HCL = "hcl"
}
export declare class FluentUIGradientPicker extends React.Component<GradientPickerProps, GradientPickerState> {
    constructor(props: GradientPickerProps);
    selectGradient(gradient: ColorGradient, emit?: boolean): void;
    render(): JSX.Element;
}
