import * as React from "react";
import { Color } from "../../core";
import { ColorPalette } from "../resources";
import { AppStore } from "../stores";
export declare function colorToCSS(color: Color): string;
export interface ColorPickerProps {
    defaultValue?: Color;
    allowNull?: boolean;
    onPick?: (color: Color) => void;
    store?: AppStore;
    parent?: React.Component;
    closePicker?: () => void;
}
export interface ColorPickerState {
    currentPalette?: ColorPalette;
    currentPicker?: string;
    currentColor?: Color;
}
export declare class ColorPicker extends React.Component<ColorPickerProps, ColorPickerState> {
    constructor(props: ColorPickerProps);
    render(): JSX.Element;
}
