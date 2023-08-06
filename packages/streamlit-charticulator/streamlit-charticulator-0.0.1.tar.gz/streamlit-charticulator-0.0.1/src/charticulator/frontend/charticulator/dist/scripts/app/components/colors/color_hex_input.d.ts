import * as React from "react";
import { ColorSpacePickerState } from "../color_space_picker";
interface ColorHexInputProps {
    state: ColorSpacePickerState;
    updateState: (state: ColorSpacePickerState) => void;
}
export declare class ColorHexInput extends React.Component<ColorHexInputProps, Record<string, unknown>> {
    render(): JSX.Element;
}
export {};
