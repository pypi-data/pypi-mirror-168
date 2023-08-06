import { ConstraintSolver } from "../../solver";
import * as Specification from "../../specification";
import { DataflowManager } from "../dataflow";
import * as Expression from "../../expression";
import * as Graphics from "../../graphics";
import { AttributeDescription, Controls, Handles, ObjectClass, ObjectClassMetadata, SnappingGuides, TemplateParameters } from "../common";
import { Color } from "../../common";
import { ChartStateManager } from "../state";
export declare abstract class ChartClass extends ObjectClass {
    readonly object: Specification.Chart;
    readonly state: Specification.ChartState;
    dataflow: DataflowManager;
    manager: ChartStateManager;
    static metadata: ObjectClassMetadata;
    setDataflow(dataflow: DataflowManager): void;
    setManager(manager: ChartStateManager): void;
    getBackgroundGraphics(): Graphics.Element;
    resolveMapping<ValueType>(mapping: Specification.Mapping, defaultValue: Specification.AttributeValue): (row: Expression.Context) => Specification.AttributeValue;
    abstract initializeState(): void;
    abstract buildIntrinsicConstraints(solver: ConstraintSolver): void;
    abstract getSnappingGuides(): SnappingGuides.Description[];
    abstract getHandles(): Handles.Description[];
}
interface RectangleChartAttributes extends Specification.AttributeMap {
    x1: number;
    y1: number;
    x2: number;
    y2: number;
    cx: number;
    cy: number;
    ox1: number;
    oy1: number;
    ox2: number;
    oy2: number;
    width: number;
    height: number;
    marginLeft: number;
    marginRight: number;
    marginTop: number;
    marginBottom: number;
    backgroundColor: Color;
}
interface RectangleChartState extends Specification.ChartState {
    attributes: RectangleChartAttributes;
}
export declare class RectangleChart extends ChartClass {
    static classID: string;
    static type: string;
    static defaultMappingValues: Specification.AttributeMap;
    static defaultProperties: Specification.AttributeMap;
    readonly object: Specification.Chart & {
        properties: {
            backgroundColor: Color;
            backgroundOpacity: number;
        };
    };
    readonly state: RectangleChartState;
    attributeNames: string[];
    attributes: {
        [name: string]: AttributeDescription;
    };
    initializeState(): void;
    getBackgroundGraphics(): Graphics.Rect;
    buildIntrinsicConstraints(solver: ConstraintSolver): void;
    getSnappingGuides(): SnappingGuides.Description[];
    getHandles(): Handles.Description[];
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
    getTemplateParameters(): TemplateParameters;
}
export declare function registerClasses(): void;
export {};
