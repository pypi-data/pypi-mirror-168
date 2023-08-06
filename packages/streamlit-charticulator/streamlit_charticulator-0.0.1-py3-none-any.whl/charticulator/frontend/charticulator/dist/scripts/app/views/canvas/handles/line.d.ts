/// <reference types="hammerjs" />
import * as React from "react";
import { Prototypes } from "../../../../core";
import { HandleViewProps } from "./common";
export interface LineHandleViewProps extends HandleViewProps {
    handle: Prototypes.Handles.Line;
}
export interface LineHandleViewState {
    dragging: boolean;
    newValue: number;
}
export declare class LineHandleView extends React.Component<LineHandleViewProps, LineHandleViewState> {
    refs: {
        line: SVGLineElement;
    };
    hammer: HammerManager;
    constructor(props: LineHandleViewProps);
    componentDidMount(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
}
