/// <reference types="hammerjs" />
import * as React from "react";
import { Prototypes } from "../../../../core";
import { HandleViewProps } from "./common";
export interface RelativeLineHandleViewProps extends HandleViewProps {
    handle: Prototypes.Handles.RelativeLine;
}
export interface RelativeLineHandleViewState {
    dragging: boolean;
    newValue: number;
}
export declare class RelativeLineHandleView extends React.Component<RelativeLineHandleViewProps, RelativeLineHandleViewState> {
    refs: {
        line: SVGLineElement;
    };
    hammer: HammerManager;
    constructor(props: RelativeLineHandleViewProps);
    componentDidMount(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
}
