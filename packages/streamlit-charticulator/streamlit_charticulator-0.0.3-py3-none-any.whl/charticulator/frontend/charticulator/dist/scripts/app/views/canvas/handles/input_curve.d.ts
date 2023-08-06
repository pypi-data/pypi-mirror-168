/// <reference types="hammerjs" />
import * as React from "react";
import { Prototypes, Point } from "../../../../core";
import { HandleViewProps } from "./common";
export interface InputCurveHandleViewProps extends HandleViewProps {
    handle: Prototypes.Handles.InputCurve;
}
export interface InputCurveHandleViewState {
    enabled: boolean;
    drawing: boolean;
    points: Point[];
}
export declare class InputCurveHandleView extends React.Component<InputCurveHandleViewProps, InputCurveHandleViewState> {
    refs: {
        interaction: SVGRectElement;
    };
    state: InputCurveHandleViewState;
    hammer: HammerManager;
    getPoint(x: number, y: number): Point;
    getBezierCurvesFromMousePoints(points: Point[]): Point[][];
    componentDidMount(): void;
    componentWillUnmount(): void;
    renderDrawing(): JSX.Element;
    renderButton(x: number, y: number): JSX.Element;
    renderSpiralButton(x: number, y: number): JSX.Element;
    render(): JSX.Element;
}
