import * as React from "react";
import { Specification, Prototypes } from "../../../../core";
import { HandleViewProps } from "./common";
export interface TextAlignmentHandleViewProps extends HandleViewProps {
    handle: Prototypes.Handles.TextAlignment;
}
export interface TextAlignmentHandleViewState {
    dragging: boolean;
    newAlignment: Specification.Types.TextAlignment;
    newRotation: number;
}
export declare class TextAlignmentHandleView extends React.Component<TextAlignmentHandleViewProps, TextAlignmentHandleViewState> {
    private container;
    private anchorCircle;
    private rotationCircle;
    private hammer;
    constructor(props: TextAlignmentHandleViewProps);
    getRelativePoint(px: number, py: number): {
        x: number;
        y: number;
    };
    componentDidMount(): void;
    componentWillUnmount(): void;
    handleClick(): void;
    getRectFromAlignment(alignment: Specification.Types.TextAlignment, rotation: number): {
        cx: number;
        cy: number;
        fx: number;
        fy: number;
        width: number;
        height: number;
        rotation: number;
    };
    renderDragging(): JSX.Element;
    render(): JSX.Element;
}
