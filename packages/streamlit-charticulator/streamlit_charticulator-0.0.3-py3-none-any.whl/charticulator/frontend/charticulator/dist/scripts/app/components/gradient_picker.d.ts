import * as React from "react";
import { Color, ColorGradient } from "../../core";
export interface GradientPickerProps {
    defaultValue?: ColorGradient;
    onPick?: (gradient: ColorGradient) => void;
}
export interface GradientPickerState {
    currentTab: string;
    currentGradient: ColorGradient;
    isPickerOpen: boolean;
    currentItemId: string;
    currentColor: Color;
    currentItemIdx: number;
}
export declare class GradientPicker extends React.Component<GradientPickerProps, GradientPickerState> {
    static tabs: {
        name: string;
        label: string;
    }[];
    constructor(props: GradientPickerProps);
    selectGradient(gradient: ColorGradient, emit?: boolean): void;
    renderGradientPalettes(): JSX.Element;
    private changeColorPickerState;
    private renderColorPicker;
    render(): JSX.Element;
}
export declare class GradientView extends React.PureComponent<{
    gradient: ColorGradient;
}, Record<string, never>> {
    protected refCanvas: HTMLCanvasElement;
    componentDidMount(): void;
    componentDidUpdate(): void;
    render(): JSX.Element;
}
