import * as Graphics from "../../graphics";
import { ConstraintSolver } from "../../solver";
import * as Specification from "../../specification";
import { AttributeDescription, BoundingBox, Controls, DropZones, Handles, ObjectClassMetadata, TemplateParameters } from "../common";
import { PlotSegmentClass } from "./plot_segment";
import { ChartStateManager } from "..";
/**
 * Line plot segment distributes the elements on the line
 *
 *  (y1 and y2 can have diferent values, so line cna have some angle between line and axis lines)
 *  y1 *------#------#------* y2
 *    x1                    x2
 *
 * # - some element on line
 */
export interface LineGuideAttributes extends Specification.AttributeMap {
    /** x value of left point of line */
    x1?: number;
    /** y value of left point of line */
    y1?: number;
    /** x value of right point of line */
    x2?: number;
    /** y value of right point of line */
    y2?: number;
    /** free variable ? TODO figure out */
    x?: number;
    /** free variable ? TODO figure out */
    y?: number;
}
export interface LineGuideState extends Specification.PlotSegmentState {
    attributes: LineGuideAttributes;
}
export interface LineGuideProperties extends Specification.AttributeMap {
    axis?: Specification.Types.AxisDataBinding;
}
export interface LineGuideObject extends Specification.PlotSegment {
    properties: LineGuideProperties;
}
export declare class LineGuide extends PlotSegmentClass {
    static classID: string;
    static type: string;
    static metadata: ObjectClassMetadata;
    static defaultProperties: Specification.AttributeMap;
    readonly state: LineGuideState;
    readonly object: LineGuideObject;
    attributeNames: string[];
    attributes: {
        [name: string]: AttributeDescription;
    };
    initializeState(): void;
    /**
     * Creates constraints for elements on the line plot segment
     * Line plot segment distributes the elements on the line
     *  (y1 and y2 can have different values, so line can have some angle between line and axis lines)
     *  *
     *  y1 *------#------#------* y2
     *    x1      t      t      x2
     *
     * # - some element on line
     * t - position of the element on line
     */
    buildGlyphConstraints(solver: ConstraintSolver): void;
    getDropZones(): DropZones.Description[];
    getHandles(): Handles.Description[];
    getBoundingBox(): BoundingBox.Description;
    getGraphics(manager: ChartStateManager): Graphics.Element;
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
    /**
     * Renders gridlines for axis. Returns empty array to diable widgets for line plot segment.
     * Not implemented yet
     * @param data axis data binding
     * @param manager widgets manager
     * @param axisProperty property name of plotsegment with axis properties (xData, yData, axis)
     */
    buildGridLineWidgets(): Controls.Widget[];
    getTemplateParameters(): TemplateParameters;
}
