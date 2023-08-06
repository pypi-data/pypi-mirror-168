import { Color } from "../../../core";
import * as React from "react";
export interface ColorGridProps {
    defaultValue?: Color;
    colors: Color[][];
    onClick?: (color: Color) => void;
}
export declare class ColorGrid extends React.PureComponent<ColorGridProps, Record<string, unknown>> {
    render(): JSX.Element;
}
