import * as React from "react";
import { Color } from "../../../core";
interface ColorGridItemProps {
    color: Color;
    defaultValue?: Color;
    onClick?: (color: Color) => void;
}
export declare class ColorGridItem extends React.Component<ColorGridItemProps, Record<string, unknown>> {
    render(): JSX.Element;
}
export {};
