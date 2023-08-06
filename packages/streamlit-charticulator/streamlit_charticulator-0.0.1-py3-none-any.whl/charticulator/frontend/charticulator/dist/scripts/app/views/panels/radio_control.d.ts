import * as React from "react";
export interface PanelRadioControlProps {
    options: string[];
    icons?: string[];
    labels?: string[];
    showText?: boolean;
    asList?: boolean;
    value?: string;
    onChange?: (newValue: string) => void;
}
export declare class PanelRadioControl extends React.Component<PanelRadioControlProps, Record<string, unknown>> {
    render(): JSX.Element;
}
