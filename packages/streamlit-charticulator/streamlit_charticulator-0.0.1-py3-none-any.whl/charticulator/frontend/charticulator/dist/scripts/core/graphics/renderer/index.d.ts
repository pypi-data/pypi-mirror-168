/**
 * See {@link ChartRenderer} for details
 *
 * @packageDocumentation
 * @preferred
 */
import { ReactElement } from "react";
import { ZoomInfo } from "../../common";
import * as Dataset from "../../dataset";
import * as Prototypes from "../../prototypes";
import * as Specification from "../../specification";
import { Group } from "../elements";
export declare function facetRows(rows: Dataset.Row[], indices: number[], columns?: string[]): number[][];
export interface RenderEvents {
    afterRendered: () => void;
}
/**
 * The class is responsible for rendering the visual part of the chart (coordinates, elements such as glyph marks e.t.c).
 * The module calls methods {@link MarkClass.getGraphics} implemented in each marks (rect, image, text, symbol e.t.c)
 *
 */
export declare class ChartRenderer {
    private manager;
    private renderEvents?;
    constructor(manager: Prototypes.ChartStateManager, renderEvents?: RenderEvents);
    /**
     * Render marks in a glyph
     * @returns an array of groups with the same size as glyph.marks
     */
    private renderGlyphMarks;
    /**
     * Method calls getGraphics method of {@link Mark} objects to get graphical representation of element
     * @param dataset Dataset of charticulator
     * @param chart Chart object
     * @param chartState State of chart and chart elements
     */
    private renderChart;
    renderControls(chart: Specification.Chart, chartState: Specification.ChartState, zoom: ZoomInfo): ReactElement<any, string | ((props: any) => ReactElement<any, string | any | (new (props: any) => import("react").Component<any, any, any>)>) | (new (props: any) => import("react").Component<any, any, any>)>[];
    render(): Group;
}
export * from "./text_measurer";
