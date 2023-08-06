import { ConstraintSolver } from "../../solver";
import * as Specification from "../../specification";
import { ChartElementClass } from "../chart_element";
import { AttributeDescription, BoundingBox, Controls, Handles, SnappingGuides } from "../common";
import { ObjectClassMetadata } from "../index";
export interface GuideCoordinatorAttributes extends Specification.AttributeMap {
    x1: number;
    y1: number;
    x2: number;
    y2: number;
    angle1: number;
    angle2: number;
    radial1: number;
    radial2: number;
    count: number;
}
export interface GuideCoordinatorProperties extends Specification.AttributeMap {
    axis: "x" | "y";
}
export declare class GuideCoordinatorClass extends ChartElementClass<GuideCoordinatorProperties, GuideCoordinatorAttributes> {
    static classID: string;
    static type: string;
    private static BaseGuidesCount;
    static metadata: ObjectClassMetadata;
    static defaultAttributes: Partial<GuideCoordinatorAttributes>;
    buildConstraints(solver: ConstraintSolver): void;
    getValueNames(): string[];
    get attributeNames(): string[];
    get attributes(): {
        [name: string]: AttributeDescription;
    };
    initializeState(): void;
    private getAxis;
    /** Get handles given current state */
    getHandles(): Handles.Description[];
    getBoundingBox(): BoundingBox.Description;
    private getBasicValues;
    getSnappingGuides(): SnappingGuides.Description[];
    /** Get controls given current state */
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
}
