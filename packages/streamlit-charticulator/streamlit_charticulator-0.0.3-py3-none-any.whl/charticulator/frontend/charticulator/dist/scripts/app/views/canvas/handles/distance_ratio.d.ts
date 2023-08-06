/// <reference types="hammerjs" />
import * as React from "react";
import { Prototypes } from "../../../../core";
import { HandleViewProps } from "./common";
export interface DistanceRatioHandleViewProps extends HandleViewProps {
    handle: Prototypes.Handles.DistanceRatio;
}
export interface DistanceRatioHandleViewState {
    dragging: boolean;
    newValue: number;
}
export declare class DistanceRatioHandleView extends React.Component<DistanceRatioHandleViewProps, DistanceRatioHandleViewState> {
    refs: {
        margin: SVGGElement;
        centerCircle: SVGCircleElement;
    };
    hammer: HammerManager;
    constructor(props: DistanceRatioHandleViewProps);
    clip(v: number): number;
    componentDidMount(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
}
