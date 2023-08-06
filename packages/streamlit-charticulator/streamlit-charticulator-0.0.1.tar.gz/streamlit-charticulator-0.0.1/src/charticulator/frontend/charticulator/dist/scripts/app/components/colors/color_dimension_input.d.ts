import * as React from "react";
interface ColorDimensionInputProps {
    title: string;
    defaultValue: number;
    range: [number, number];
    updateState: (state: number) => void;
}
export declare class ColorDimensionInput extends React.Component<ColorDimensionInputProps, Record<string, unknown>> {
    render(): JSX.Element;
}
export {};
