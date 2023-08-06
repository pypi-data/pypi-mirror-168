import * as React from "react";
import { ColorPickerState } from "../fluentui_color_picker";
export declare enum PickerType {
    HCL = "hcl",
    HSV = "hsv"
}
interface ColorPickerButtonProps {
    state: ColorPickerState;
    onClick: () => void;
    type: PickerType;
}
export declare class ColorPickerButton extends React.Component<ColorPickerButtonProps, Record<string, unknown>> {
    render(): JSX.Element;
}
export {};
