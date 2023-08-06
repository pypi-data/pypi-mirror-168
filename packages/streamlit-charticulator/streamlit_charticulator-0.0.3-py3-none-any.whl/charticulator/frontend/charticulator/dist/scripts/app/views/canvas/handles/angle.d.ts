/// <reference types="hammerjs" />
import * as React from "react";
import { Prototypes } from "../../../../core";
import { HandleViewProps } from "./common";
export interface AngleHandleViewProps extends HandleViewProps {
    handle: Prototypes.Handles.Angle;
}
export interface AngleHandleViewState {
    dragging: boolean;
    newValue: number;
}
export declare class AngleHandleView extends React.Component<AngleHandleViewProps, AngleHandleViewState> {
    refs: {
        margin: SVGGElement;
        centerCircle: SVGCircleElement;
    };
    hammer: HammerManager;
    constructor(props: AngleHandleViewProps);
    clipAngle(v: number): number;
    componentDidMount(): void;
    componentWillUnmount(): void;
    static shapeCircle: (r: number) => string;
    static shapeRight: (r: number) => string;
    static shapeLeft: (r: number) => string;
    render(): JSX.Element;
}
