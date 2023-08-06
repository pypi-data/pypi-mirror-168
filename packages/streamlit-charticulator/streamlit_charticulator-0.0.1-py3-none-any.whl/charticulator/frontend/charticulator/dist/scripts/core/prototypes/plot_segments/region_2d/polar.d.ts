import * as Graphics from "../../../graphics";
import { ConstraintSolver } from "../../../solver";
import * as Specification from "../../../specification";
import { AttributeDescription, BoundingBox, BuildConstraintsContext, Controls, DropZones, Handles, ObjectClassMetadata, SnappingGuides, TemplateParameters } from "../../common";
import { Region2DAttributes, Region2DConfigurationIcons, Region2DConstraintBuilder, Region2DProperties } from "./base";
import { PlotSegmentClass } from "../plot_segment";
import { ChartStateManager } from "../..";
export declare type PolarAxisMode = "null" | "default" | "numerical" | "categorical";
export interface PolarAttributes extends Region2DAttributes {
    /** Cartesian plot segment region */
    x1: number;
    y1: number;
    x2: number;
    y2: number;
    cx: number;
    cy: number;
    angle1: number;
    angle2: number;
    radial1: number;
    radial2: number;
    a1r1x: number;
    a1r1y: number;
    a1r2x: number;
    a1r2y: number;
    a2r1x: number;
    a2r1y: number;
    a2r2x: number;
    a2r2y: number;
}
export interface PolarState extends Specification.PlotSegmentState {
    attributes: PolarAttributes;
}
export interface PolarProperties extends Region2DProperties {
    startAngle: number;
    endAngle: number;
    innerRatio: number;
    outerRatio: number;
    equalizeArea: boolean;
    autoAlignment: boolean;
}
export interface PolarObject extends Specification.PlotSegment {
    properties: PolarProperties;
}
export declare const icons: Region2DConfigurationIcons;
export declare class PolarPlotSegment extends PlotSegmentClass<PolarProperties, PolarAttributes> {
    static classID: string;
    static type: string;
    static metadata: ObjectClassMetadata;
    static defaultProperties: Specification.AttributeMap;
    readonly state: PolarState;
    readonly object: PolarObject;
    attributeNames: string[];
    attributes: {
        [name: string]: AttributeDescription;
    };
    initializeState(): void;
    createBuilder(solver?: ConstraintSolver, context?: BuildConstraintsContext): Region2DConstraintBuilder;
    buildConstraints(solver: ConstraintSolver, context: BuildConstraintsContext, manager: ChartStateManager): void;
    buildGlyphConstraints(solver: ConstraintSolver, context: BuildConstraintsContext): void;
    getBoundingBox(): BoundingBox.Description;
    getSnappingGuides(): SnappingGuides.Description[];
    getGraphics(manager: ChartStateManager): Graphics.Group;
    getPlotSegmentBackgroundGraphics(manager: ChartStateManager): Graphics.Group;
    getCoordinateSystem(): Graphics.CoordinateSystem;
    getDropZones(): DropZones.Description[];
    getAxisModes(): [PolarAxisMode, PolarAxisMode];
    getHandles(): Handles.Description[];
    getPopupEditor(manager: Controls.WidgetManager): Controls.PopupEditor;
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
    getTemplateParameters(): TemplateParameters;
}
