/// <reference types="hammerjs" />
import * as React from "react";
import { Prototypes } from "../../../../core";
import { HandleViewProps } from "./common";
export interface PointHandleViewProps extends HandleViewProps {
    handle: Prototypes.Handles.Point;
}
export interface PointHandleViewState {
    dragging: boolean;
    newXValue: number;
    newYValue: number;
}
export declare class PointHandleView extends React.Component<PointHandleViewProps, PointHandleViewState> {
    refs: {
        circle: SVGCircleElement;
    };
    hammer: HammerManager;
    constructor(props: PointHandleViewProps);
    componentDidMount(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
}
