/// <reference types="hammerjs" />
import * as React from "react";
import { EventSubscription, Graphics, Point, Specification, ZoomInfo } from "../../../core";
import { DragData } from "../../actions";
import { DragContext, Droppable } from "../../controllers";
import { AppStore, Selection } from "../../stores";
import { ChartSnappableGuide } from "./snapping/chart";
export interface ChartEditorViewProps {
    store: AppStore;
}
export interface ChartEditorViewState {
    viewWidth: number;
    viewHeight: number;
    zoom: ZoomInfo;
    snappingCandidates: ChartSnappableGuide[] | null;
    graphics: Graphics.Element;
    currentCreation?: string;
    currentCreationOptions?: string;
    currentSelection: Selection;
    dropZoneData: {
        data?: DragData.DropZoneData;
        layout?: DragData.ScaffoldType;
    } | false;
    isSolving: boolean;
    canvasToolbar: boolean;
}
/**
 * Editor view for chart
 * ![Mark widgets](media://chart_editor.png)
 */
export declare class ChartEditorView extends React.Component<ChartEditorViewProps, ChartEditorViewState> implements Droppable {
    refs: {
        canvasContainer: HTMLDivElement;
        canvas: SVGElement;
        canvasInteraction: SVGRectElement;
    };
    protected tokens: EventSubscription[];
    protected hammer: HammerManager;
    constructor(props: ChartEditorViewProps);
    getRelativePoint(point: Point): Point;
    getFitViewZoom(width: number, height: number): ZoomInfo;
    componentDidMount(): void;
    componentWillUnmount(): void;
    onDragEnter(ctx: DragContext): boolean;
    protected getGraphics(): Graphics.Element;
    protected updateSelection(): void;
    protected updateGraphics(): void;
    renderGraphics(): JSX.Element;
    renderEditingLink(): JSX.Element;
    renderCreatingComponent(): JSX.Element;
    doCustomZoom(cx: number, cy: number, width: number, height: number): void;
    renderBoundsGuides(): JSX.Element[];
    getSnappingGuides(): ChartSnappableGuide[];
    renderChartHandles(): JSX.Element[];
    renderMarkHandlesInPlotSegment(plotSegment: Specification.PlotSegment, plotSegmentState: Specification.PlotSegmentState): JSX.Element;
    renderLayoutHandles(): JSX.Element[];
    renderHandles(): JSX.Element;
    renderControls(): JSX.Element;
    renderSnappingGuides(): JSX.Element[];
    renderChartCanvas(): JSX.Element;
    renderDropZoneForMarkLayout(layout: Specification.PlotSegment, state: Specification.PlotSegmentState): JSX.Element[];
    renderDropZones(): JSX.Element;
    doZoom(factor: number): void;
    render(): JSX.Element;
}
