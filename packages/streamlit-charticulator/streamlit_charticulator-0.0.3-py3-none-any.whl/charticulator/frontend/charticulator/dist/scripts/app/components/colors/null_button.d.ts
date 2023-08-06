import * as React from "react";
import { Color } from "../../../core";
interface NullButtonProps {
    allowNull?: boolean;
    onPick: (color: Color) => void;
}
export declare class NullButton extends React.Component<NullButtonProps, Record<string, unknown>> {
    render(): JSX.Element;
}
export {};
