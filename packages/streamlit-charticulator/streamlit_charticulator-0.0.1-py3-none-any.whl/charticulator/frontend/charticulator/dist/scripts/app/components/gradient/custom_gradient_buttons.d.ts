import * as React from "react";
import { ColorGradient } from "../../../core";
interface CustomGradientButtonsProps {
    currentGradient: ColorGradient;
    selectGradient: (gradient: ColorGradient, emit: boolean) => void;
}
export declare class CustomGradientButtons extends React.Component<CustomGradientButtonsProps, Record<string, unknown>> {
    render(): JSX.Element;
}
export {};
