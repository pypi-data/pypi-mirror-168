import * as React from "react";
import { Color } from "../../../core";
import { ColorSpaceDescription, ColorSpacePickerState } from "../color_space_picker";
interface ColorSpaceSelectProps {
    onChange?: (newValue: Color) => void;
    colorSpaces: ColorSpaceDescription[];
    state: ColorSpacePickerState;
    updateState: (state: ColorSpacePickerState) => void;
}
export declare class ColorSpaceSelect extends React.Component<ColorSpaceSelectProps, Record<string, unknown>> {
    render(): JSX.Element;
}
export {};
