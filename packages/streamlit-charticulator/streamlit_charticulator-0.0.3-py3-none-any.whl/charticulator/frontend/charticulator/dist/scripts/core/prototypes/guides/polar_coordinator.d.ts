import { ConstraintSolver } from "../../solver";
import * as Specification from "../../specification";
import { ObjectState } from "../../specification";
import { ChartElementClass } from "../chart_element";
import { AttributeDescription, Handles, SnappingGuides, BoundingBox, Controls } from "../common";
import { ObjectClassMetadata } from "../index";
import { Region2DAttributes } from "../plot_segments";
import { ChartStateManager } from "../state";
export interface PolarGuideCoordinatorAttributesExtend extends Region2DAttributes {
    x: number;
    y: number;
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
}
export interface PolarGuideCoordinatorAttributes extends PolarGuideCoordinatorAttributesExtend, Specification.AttributeMap {
}
export interface PolarGuideState extends ObjectState<PolarGuideCoordinatorAttributes> {
    attributes: PolarGuideCoordinatorAttributes;
}
interface PolarGuideCoordinatorPropertiesExtend {
    startAngle: number;
    endAngle: number;
    innerRatio: number;
    outerRatio: number;
    angularGuidesCount: number;
    radialGuidesCount: number;
}
export interface PolarGuideCoordinatorProperties extends PolarGuideCoordinatorPropertiesExtend, Specification.AttributeMap {
}
export declare const PolarGuidePropertyNames: Extract<keyof PolarGuideCoordinatorPropertiesExtend, string>[];
export interface GuidePolarCoordinatorProperties extends Specification.AttributeMap {
    properties: PolarGuideCoordinatorProperties;
}
export interface PolarGuideObject extends Specification.Object<PolarGuideCoordinatorProperties> {
    properties: PolarGuideCoordinatorProperties;
}
export declare const PolarGuideBaseAttributeNames: Extract<keyof PolarGuideCoordinatorAttributes, string>[];
export declare const getAngularValueName: (index: number) => string;
export declare const getRadialValueName: (index: number) => string;
export declare const getPointValueName: (angularIndex: number, radialIndex: number, axis: "X" | "Y") => string;
export declare class GuidePolarCoordinatorClass extends ChartElementClass<PolarGuideCoordinatorProperties, PolarGuideCoordinatorAttributes> {
    static classID: string;
    static type: string;
    static metadata: ObjectClassMetadata;
    readonly state: PolarGuideState;
    static defaultAttributes: Partial<PolarGuideCoordinatorAttributes>;
    buildConstraints(solver: ConstraintSolver, constr: any, manager: ChartStateManager): void;
    getValueNamesForAngular(): string[];
    getValueNamesForRadial(): string[];
    getValueNamesForPoints(): string[];
    get attributeNames(): string[];
    get attributes(): {
        [name: string]: AttributeDescription;
    };
    initializeState(): void;
    /** Get handles given current state */
    getHandles(): Handles.Description[];
    getBoundingBox(): BoundingBox.Circle;
    getSnappingGuides(): SnappingGuides.PolarAxis[];
    /** Get controls given current state */
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
}
export {};
