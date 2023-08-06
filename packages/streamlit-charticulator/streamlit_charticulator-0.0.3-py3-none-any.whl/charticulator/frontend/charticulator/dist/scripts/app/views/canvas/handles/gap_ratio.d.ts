/// <reference types="hammerjs" />
import * as React from "react";
import { Prototypes } from "../../../../core";
import { HandleViewProps } from "./common";
export interface RelativeLineRatioHandleViewProps extends HandleViewProps {
    handle: Prototypes.Handles.GapRatio;
}
export interface RelativeLineRatioHandleViewState {
    dragging: boolean;
    newValue: number;
}
export declare class GapRatioHandleView extends React.Component<RelativeLineRatioHandleViewProps, RelativeLineRatioHandleViewState> {
    refs: {
        cOrigin: SVGCircleElement;
        line: SVGLineElement;
    };
    hammer: HammerManager;
    constructor(props: RelativeLineRatioHandleViewProps);
    componentDidMount(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
    renderPolar(): JSX.Element;
    renderCartesian(): JSX.Element;
}
