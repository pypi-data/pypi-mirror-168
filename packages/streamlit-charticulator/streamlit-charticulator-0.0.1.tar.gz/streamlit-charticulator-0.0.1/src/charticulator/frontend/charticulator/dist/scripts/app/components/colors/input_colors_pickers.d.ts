import * as React from "react";
import { Color } from "../../../core";
import { ColorSpaceDescription } from "../color_space_picker";
export declare class HCLColorPicker extends React.Component<{
    defaultValue: Color;
    onChange?: (newValue: Color) => void;
}, Record<string, unknown>> {
    static colorSpaces: ColorSpaceDescription[];
    render(): JSX.Element;
}
export declare class HSVColorPicker extends React.Component<{
    defaultValue: Color;
    onChange?: (newValue: Color) => void;
}, Record<string, unknown>> {
    static colorSpaces: ColorSpaceDescription[];
    render(): JSX.Element;
}
