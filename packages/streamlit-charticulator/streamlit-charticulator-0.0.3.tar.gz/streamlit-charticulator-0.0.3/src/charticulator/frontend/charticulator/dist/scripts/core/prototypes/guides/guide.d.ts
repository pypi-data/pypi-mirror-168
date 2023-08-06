import { ConstraintSolver } from "../../solver";
import * as Specification from "../../specification";
import { ChartElementClass } from "../chart_element";
import { AttributeDescription, Controls, Handles, LinkAnchor, SnappingGuides, TemplateParameters } from "../common";
import { ObjectClassMetadata } from "../index";
export declare type GuideAxis = "x" | "y";
export declare enum GuideAttributeNames {
    value = "value",
    computedBaselineValue = "computedBaselineValue"
}
export interface GuideAttributes extends Specification.AttributeMap {
    value: number;
    computedBaselineValue: number;
}
interface GuideAttributeDescription extends AttributeDescription {
    name: GuideAttributeNames;
}
export declare enum GuidePropertyNames {
    axis = "axis",
    baseline = "baseline"
}
export interface GuideProperties extends Specification.AttributeMap {
    axis: GuideAxis;
    baseline: Specification.baselineH | Specification.baselineV;
}
export declare class GuideClass extends ChartElementClass<GuideProperties, GuideAttributes> {
    static classID: string;
    static type: string;
    static metadata: ObjectClassMetadata;
    static defaultProperties: Partial<GuideProperties>;
    attributeNames: GuideAttributeNames[];
    attributes: {
        [name in GuideAttributeNames]: GuideAttributeDescription;
    };
    initializeState(): void;
    private getAxis;
    private getParentType;
    buildConstraints(solver: ConstraintSolver): void;
    private computeBaselineFromParentAttribute;
    getLinkAnchors(): LinkAnchor.Description[];
    /** Get handles given current state */
    getHandles(): Handles.Description[];
    getSnappingGuides(): SnappingGuides.Description[];
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
    getTemplateParameters(): TemplateParameters;
}
export {};
