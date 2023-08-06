/// <reference types="hammerjs" />
import * as React from "react";
import { ZoomInfo } from "../../../../core";
export interface ResizeHandleViewProps {
    width: number;
    height: number;
    cx: number;
    cy: number;
    zoom: ZoomInfo;
    onResize: (width: number, height: number) => void;
}
export interface ResizeHandleViewState {
    dragging: boolean;
    newX1: number;
    newY1: number;
    newX2: number;
    newY2: number;
}
export declare class ResizeHandleView extends React.Component<ResizeHandleViewProps, ResizeHandleViewState> {
    refs: {
        container: SVGGElement;
        lineX1: SVGLineElement;
        lineX2: SVGLineElement;
        lineY1: SVGLineElement;
        lineY2: SVGLineElement;
        cornerX1Y1: SVGCircleElement;
        cornerX1Y2: SVGCircleElement;
        cornerX2Y1: SVGCircleElement;
        cornerX2Y2: SVGCircleElement;
    };
    state: ResizeHandleViewState;
    hammer: HammerManager;
    componentDidMount(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
}
