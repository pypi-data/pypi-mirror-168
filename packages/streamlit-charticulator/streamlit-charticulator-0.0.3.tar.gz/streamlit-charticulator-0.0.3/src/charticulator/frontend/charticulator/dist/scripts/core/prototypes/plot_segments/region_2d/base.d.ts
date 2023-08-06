import * as Expression from "../../../expression";
import { ConstraintSolver, ConstraintStrength, Variable } from "../../../solver";
import * as Specification from "../../../specification";
import { BuildConstraintsContext, Controls } from "../../common";
import { DataflowTable } from "../../dataflow";
import { AxisMode } from "../axis";
import { PlotSegmentClass } from "../plot_segment";
import { ChartStateManager } from "../../state";
export declare enum Region2DSublayoutType {
    Overlap = "overlap",
    DodgeX = "dodge-x",
    DodgeY = "dodge-y",
    Grid = "grid",
    Packing = "packing",
    Jitter = "jitter"
}
export declare enum SublayoutAlignment {
    Start = "start",
    Middle = "middle",
    End = "end"
}
export declare enum GridDirection {
    X = "x",
    Y = "y"
}
export declare enum GridStartPosition {
    LeftTop = "LT",
    RightTop = "RT",
    LeftBottom = "LB",
    RigtBottom = "RB"
}
export interface Region2DSublayoutOptions extends Specification.AttributeMap {
    type: Region2DSublayoutType;
    /** Sublayout alignment (for dodge and grid) */
    align: {
        x: SublayoutAlignment;
        y: SublayoutAlignment;
    };
    ratioX: number;
    ratioY: number;
    /** Grid options */
    grid?: {
        /** Grid direction */
        direction: GridDirection;
        /** Number of glyphs in X direction (direction == "x") */
        xCount?: number;
        /** Number of glyphs in Y direction (direction == "x") */
        yCount?: number;
        /** Position of the first glyph in grid */
        gridStartPosition: GridStartPosition;
    };
    /** Order in sublayout objects */
    order: Specification.Types.SortBy;
    orderReversed: boolean;
    /** packing options */
    packing: {
        gravityX: number;
        gravityY: number;
        boxedX: boolean;
        boxedY: boolean;
    };
    jitter: {
        vertical: boolean;
        horizontal: boolean;
    };
}
export interface Region2DAttributes extends Specification.AttributeMap {
    /** Horizontal/vertical line guide line position */
    x?: number;
    y?: number;
    gapX?: number;
    gapY?: number;
}
export interface Region2DHandleDescription {
    type: "gap";
    gap?: {
        property: Controls.Property;
        axis: AxisMode;
        reference: number;
        value: number;
        span: [number, number];
        scale: number;
    };
}
export declare enum PlotSegmentAxisPropertyNames {
    xData = "xData",
    yData = "yData",
    axis = "axis"
}
export interface Region2DProperties extends Specification.AttributeMap {
    /** X axis data binding, set to null to remove the axis, set to { type: "none" } to keep the axis but don't bind data */
    xData?: Specification.Types.AxisDataBinding;
    /** Y axis data binding, set to null to remove the axis, set to { type: "none" } to keep the axis but don't bind data */
    yData?: Specification.Types.AxisDataBinding;
    sublayout: Region2DSublayoutOptions;
    marginX1?: number;
    marginX2?: number;
    marginY1?: number;
    marginY2?: number;
}
export interface Region2DConfigurationTerminology {
    xAxis: string;
    yAxis: string;
    /** Items alignments */
    xMin: string;
    xMiddle: string;
    xMax: string;
    yMin: string;
    yMiddle: string;
    yMax: string;
    /** Stack X */
    dodgeX: string;
    /** Stack Y */
    dodgeY: string;
    /** Grid */
    grid: string;
    gridDirectionX: string;
    gridDirectionY: string;
    /** Packing force layout */
    packing: string;
    overlap: string;
    jitter: string;
}
export interface Region2DConfigurationIcons {
    xMinIcon: string;
    xMiddleIcon: string;
    xMaxIcon: string;
    yMinIcon: string;
    yMiddleIcon: string;
    yMaxIcon: string;
    dodgeXIcon: string;
    dodgeYIcon: string;
    gridIcon: string;
    packingIcon: string;
    jitterIcon: string;
    overlapIcon: string;
}
export interface Region2DConfiguration {
    terminology: Region2DConfigurationTerminology;
    icons: Region2DConfigurationIcons;
    xAxisPrePostGap: boolean;
    yAxisPrePostGap: boolean;
    getXYScale?(): {
        x: number;
        y: number;
    };
}
export declare class CrossFitter {
    private solver;
    private mode;
    private candidates;
    constructor(solver: ConstraintSolver, mode: "min" | "max");
    add(src: Variable, dst: Variable): void;
    addComplex(src: Variable, dst: [number, Variable][], dstBias?: number): void;
    addConstraint(w: ConstraintStrength): void;
}
export declare class DodgingFitters {
    xMin: CrossFitter;
    xMax: CrossFitter;
    yMin: CrossFitter;
    yMax: CrossFitter;
    constructor(solver: ConstraintSolver);
    addConstraint(w: ConstraintStrength): void;
}
/**
 * Describes variables for constraints group. Count of group matches with data cound
 */
export declare class SublayoutGroup {
    group: number[];
    x1: Variable;
    y1: Variable;
    x2: Variable;
    y2: Variable;
}
export interface SublayoutContext {
    mode: "default" | "x-only" | "y-only" | "disabled";
    xAxisPrePostGap?: boolean;
    yAxisPrePostGap?: boolean;
}
/**
 * Class builds constrains for plot segments
 * The builder creates constraints depends on sublayout
 */
export declare class Region2DConstraintBuilder {
    plotSegment: PlotSegmentClass<Region2DProperties, Region2DAttributes>;
    config: Region2DConfiguration;
    x1Name: string;
    x2Name: string;
    y1Name: string;
    y2Name: string;
    solver?: ConstraintSolver;
    solverContext?: BuildConstraintsContext;
    chartStateManager?: ChartStateManager;
    constructor(plotSegment: PlotSegmentClass<Region2DProperties, Region2DAttributes>, config: Region2DConfiguration, x1Name: string, x2Name: string, y1Name: string, y2Name: string, solver?: ConstraintSolver, solverContext?: BuildConstraintsContext, chartStateManager?: ChartStateManager);
    static defaultJitterPackingRadius: number;
    getTableContext(): DataflowTable;
    getExpression(expr: string): Expression.Expression;
    groupMarksByCategories(categories: {
        expression: string;
        categories: string[];
    }[]): number[][];
    orderMarkGroups(groups: SublayoutGroup[]): SublayoutGroup[];
    /** Make sure gapX correctly correspond to gapXRatio */
    gapX(length: number, ratio: number): void;
    /** Make sure gapY correctly correspond to gapYRatio */
    gapY(length: number, ratio: number): void;
    /**
     * Map elements according to numerical/categorical mapping
     */
    numericalMapping(axis: AxisMode): void;
    private numericalMappingY;
    private numericalMappingX;
    groupMarksByCategoricalMapping(axis: "x" | "y" | "xy"): number[][];
    categoricalMapping(axis: "x" | "y" | "xy", sublayoutContext: SublayoutContext): void;
    private categoricalMappingXY;
    private categoricalMappingY;
    private categoricalMappingX;
    categoricalHandles(axis: "x" | "y" | "xy", sublayout: boolean): Region2DHandleDescription[];
    stacking(axis: AxisMode): void;
    private stackingY;
    private stackingX;
    fitGroups(groups: SublayoutGroup[], axis: "x" | "y" | "xy"): void;
    applySublayout(groups: SublayoutGroup[], axis: "x" | "y" | "xy", context: SublayoutContext): void;
    sublayoutDodging(groups: SublayoutGroup[], direction: GridDirection, enablePrePostGap: boolean): void;
    private setSublayoutDodgingDirectionY;
    private setSublayoutDodgingDirectionX;
    private setFirstSublayoutDodgingDirection;
    getGlyphPreSolveAttributes(rowIndices: number[]): {
        [name: string]: number;
    };
    sublayoutGrid(groups: SublayoutGroup[], directionOverride?: string): void;
    private addGlyphConstraints;
    sublayoutHandles(groups: {
        group: number[];
        x1: number;
        y1: number;
        x2: number;
        y2: number;
    }[], enablePrePostGapX: boolean, enablePrePostGapY: boolean): Region2DHandleDescription[];
    sublayoutPacking(groups: SublayoutGroup[], axisOnly?: AxisMode): void;
    sublayoutJitter(groups: SublayoutGroup[], axisOnly?: AxisMode): void;
    getHandles(): Region2DHandleDescription[];
    build(): void;
    private buildXCategoricalMode;
    private buildXNumericalMode;
    private buildXDefaultMode;
    private buildXNullMode;
    applicableSublayoutOptions(): {
        value: Region2DSublayoutType;
        label: string;
        icon: string;
    }[];
    isSublayoutApplicable(): boolean;
    buildSublayoutWidgets(m: Controls.WidgetManager): any[];
    buildAxisWidgets(manager: Controls.WidgetManager, axisName: string, axis: "x" | "y"): Controls.Widget[];
    updatePlotSegment(): void;
    buildPanelWidgets(m: Controls.WidgetManager): Controls.Widget[];
    buildPopupWidgets(m: Controls.WidgetManager): Controls.Widget[];
}
