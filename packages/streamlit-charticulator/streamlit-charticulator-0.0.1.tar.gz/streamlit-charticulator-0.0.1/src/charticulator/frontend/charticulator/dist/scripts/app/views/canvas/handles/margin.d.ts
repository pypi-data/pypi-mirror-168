/// <reference types="hammerjs" />
import * as React from "react";
import { Prototypes } from "../../../../core";
import { HandleViewProps } from "./common";
export interface MarginHandleViewProps extends HandleViewProps {
    handle: Prototypes.Handles.Margin;
}
export interface MarginHandleViewState {
    dragging: boolean;
    newValue: number;
}
export declare class MarginHandleView extends React.Component<MarginHandleViewProps, MarginHandleViewState> {
    refs: {
        margin: SVGGElement;
    };
    hammer: HammerManager;
    constructor(props: MarginHandleViewProps);
    componentDidMount(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
}
