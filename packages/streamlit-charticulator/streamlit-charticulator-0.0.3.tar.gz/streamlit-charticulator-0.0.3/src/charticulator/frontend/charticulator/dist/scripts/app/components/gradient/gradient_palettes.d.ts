import * as React from "react";
import { ColorGradient } from "../../../core";
interface GradientPalettesProps {
    selectGradient: (gradient: ColorGradient, emit: boolean) => void;
}
export declare class GradientPalettes extends React.Component<GradientPalettesProps, Record<string, unknown>> {
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
export {};
