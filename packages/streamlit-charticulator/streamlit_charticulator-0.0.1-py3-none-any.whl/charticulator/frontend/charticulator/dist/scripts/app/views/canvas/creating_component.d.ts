/// <reference types="hammerjs" />
import * as React from "react";
import { Point, ZoomInfo, Specification, Prototypes } from "../../../core";
import { SnappableGuide } from "./snapping/common";
export interface CreatingComponentProps {
    width: number;
    height: number;
    zoom: ZoomInfo;
    guides: SnappableGuide<any>[];
    mode: string;
    onCreate: (...args: [number, Specification.Mapping][]) => void;
    onCancel: () => void;
}
export interface CreatingComponentState {
    points?: Point[];
    draggingPoint?: Point;
    activeGuides: SnappableGuide<any>[];
    hoverCandidateX: [number, Specification.Mapping];
    hoverCandidateY: [number, Specification.Mapping];
}
export declare class PointSnapping {
    threshold: number;
    guides: SnappableGuide<any>[];
    snappedGuides: Set<SnappableGuide<any>>;
    constructor(guides: SnappableGuide<any>[], threshold?: number);
    beginSnapping(): void;
    snapXValue(x: number): [number, Specification.Mapping];
    snapYValue(y: number): [number, Specification.Mapping];
    endSnapping(): Set<SnappableGuide<any>>;
}
export declare class CreatingComponent extends React.Component<CreatingComponentProps, CreatingComponentState> {
    refs: {
        handler: SVGRectElement;
    };
    hammer: HammerManager;
    private mode;
    constructor(props: CreatingComponentProps);
    getPointFromEvent(point: Point): Point;
    private isHammering;
    private initHammer;
    componentDidUpdate(): void;
    componentDidMount(): void;
    componentWillUnmount(): void;
    getPixelPoint(p: Point): Point;
    renderHint(): JSX.Element;
    renderSnappingGuides(): JSX.Element[];
    render(): JSX.Element;
}
export interface CreatingComponentFromCreatingInteractionProps {
    width: number;
    height: number;
    zoom: ZoomInfo;
    guides: SnappableGuide<any>[];
    description: Prototypes.CreatingInteraction.Description;
    onCreate: (mappings: {
        [name: string]: [number, Specification.Mapping];
    }, attributes: {
        [name: string]: Specification.AttributeValue;
    }) => void;
    onCancel: () => void;
}
export declare class CreatingComponentFromCreatingInteraction extends React.Component<CreatingComponentFromCreatingInteractionProps, Record<string, unknown>> {
    doCreate(inMappings: {
        [name: string]: [number, Specification.Mapping];
    }): void;
    render(): JSX.Element;
}
