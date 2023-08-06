import * as React from "react";
import { ColorSpacePickerState } from "../color_space_picker";
interface ColorRgbInputProps {
    state: ColorSpacePickerState;
    updateState: (state: ColorSpacePickerState) => void;
}
export declare class ColorRgbInput extends React.Component<ColorRgbInputProps, Record<string, unknown>> {
    private transformColorValue;
    render(): JSX.Element;
}
export {};
