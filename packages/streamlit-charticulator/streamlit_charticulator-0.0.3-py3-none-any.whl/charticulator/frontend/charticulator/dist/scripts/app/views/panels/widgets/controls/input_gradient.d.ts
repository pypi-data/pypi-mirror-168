import { ColorGradient } from "../../../../../core";
import * as React from "react";
export interface InputColorGradientProps {
    defaultValue: ColorGradient;
    onEnter: (value: ColorGradient) => boolean;
}
export declare class InputColorGradient extends React.Component<InputColorGradientProps, Record<string, unknown>> {
    render(): JSX.Element;
}
