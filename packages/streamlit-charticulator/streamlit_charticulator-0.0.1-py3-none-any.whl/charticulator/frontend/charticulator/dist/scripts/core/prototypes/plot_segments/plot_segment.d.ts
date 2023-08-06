import { ChartStateManager } from "..";
import * as Graphics from "../../graphics";
import { ConstraintSolver } from "../../solver";
import * as Specification from "../../specification";
import { BuildConstraintsContext, ChartElementClass } from "../chart_element";
import { BoundingBox, Controls, DropZones, Handles } from "../common";
import { ZoomInfo } from "../..";
import { ReactElement } from "react";
export declare abstract class PlotSegmentClass<PropertiesType extends Specification.AttributeMap = Specification.AttributeMap, AttributesType extends Specification.AttributeMap = Specification.AttributeMap> extends ChartElementClass<PropertiesType, AttributesType> {
    readonly object: Specification.PlotSegment<PropertiesType>;
    readonly state: Specification.PlotSegmentState<AttributesType>;
    /** Fill the layout's default state */
    initializeState(): void;
    /** Build intrinsic constraints between attributes (e.g., x2 - x1 = width for rectangles) */
    buildConstraints(solver: ConstraintSolver, context: BuildConstraintsContext, manager: ChartStateManager): void;
    /** Build constraints for glyphs within */
    buildGlyphConstraints(solver: ConstraintSolver, context: BuildConstraintsContext): void;
    /** Get the graphics that represent this layout */
    getPlotSegmentGraphics(glyphGraphics: Graphics.Element, manager: ChartStateManager): Graphics.Element;
    /** Get the graphics that represent this layout of elements in background*/
    getPlotSegmentBackgroundGraphics(manager: ChartStateManager): Graphics.Element;
    renderControls(_manager: ChartStateManager, _zoom: ZoomInfo): ReactElement<any>[];
    getCoordinateSystem(): Graphics.CoordinateSystem;
    /** Get DropZones given current state */
    getDropZones(): DropZones.Description[];
    /** Get handles given current state */
    getHandles(): Handles.Description[];
    getBoundingBox(): BoundingBox.Description;
    /**
     * Renders gridlines for axis
     * @param data axis data binding
     * @param manager widgets manager
     * @param axisProperty property name of plotsegment with axis properties (xData, yData, axis)
     */
    buildGridLineWidgets(data: Specification.Types.AxisDataBinding, manager: Controls.WidgetManager, axisProperty: string, mainCollapsePanelHeader: string): any[];
    static getGridLineAttributePanelWidgets(manager: Controls.WidgetManager, axisProperty: string, mainCollapsePanelHeader?: string): any[];
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
    static createDefault(glyph: Specification.Glyph): Specification.PlotSegment;
    getDisplayRawFormat(binding: Specification.Types.AxisDataBinding, manager: ChartStateManager): (value: any) => any;
    getDisplayFormat: (binding: Specification.Types.AxisDataBinding, tickFormat?: string, manager?: ChartStateManager) => (value: any) => any;
    protected buildGlyphOrderedList(): number[];
    /**
     * Return the index of the first glyph after sorting glyphs according sublayout order parameter
     */
    getFirstGlyphIndex(): number;
    /**
     * Return the index of the last glyph after sorting glyphs according sublayout order parameter
     */
    getLastGlyphIndex(): number;
}
