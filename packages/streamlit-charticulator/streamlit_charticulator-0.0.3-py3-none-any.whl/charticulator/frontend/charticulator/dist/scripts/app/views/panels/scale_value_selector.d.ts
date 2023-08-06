import * as React from "react";
import { EventSubscription, Specification } from "../../../core";
import { AppStore } from "../../stores";
export interface ScaleValueSelectorProps {
    scale: Specification.Scale;
    scaleMapping: Specification.ScaleMapping;
    store: AppStore;
    onSelect?: (index: number) => void;
}
export interface ScaleValueSelectorState {
    selectedIndex: number;
}
export declare class ScaleValueSelector extends React.Component<ScaleValueSelectorProps, ScaleValueSelectorState> {
    token: EventSubscription;
    constructor(props: ScaleValueSelectorProps);
    componentDidMount(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
}
