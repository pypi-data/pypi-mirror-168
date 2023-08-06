import * as React from "react";
import { Color, ColorGradient } from "../../../core";
interface CustomGradientMenuProps {
    currentGradient: ColorGradient;
    selectGradient: (gradient: ColorGradient, emit: boolean) => void;
}
interface CustomGradientMenuState {
    isPickerOpen: boolean;
    currentItemId: string;
    currentColor: Color;
    currentItemIdx: number;
}
export declare class CustomGradientMenu extends React.Component<CustomGradientMenuProps, CustomGradientMenuState> {
    constructor(props: CustomGradientMenuProps);
    render(): JSX.Element;
    private changeColorPickerState;
    private renderColorPicker;
}
export {};
