import { CharticulatorPropertyAccessors } from "../../../app/views/panels/widgets/types";
import { Prototypes } from "../../../container";
import { Color } from "../../common";
import * as Specification from "../../specification";
import { ChartElementClass } from "../chart_element";
import { AttributeDescription, BoundingBox, Controls, Handles, ObjectClassMetadata, TemplateParameters } from "../common";
export interface LegendAttributes extends Specification.AttributeMap {
    x: number;
    y: number;
}
export interface LegendProperties extends Specification.AttributeMap {
    scale: string;
    alignX: string;
    alignY: string;
    fontFamily: string;
    fontSize: number;
    textColor: Color;
    order: string[];
    markerShape: "rectangle" | "circle" | "triangle";
}
export interface LegendState extends Specification.ObjectState {
    attributes: LegendAttributes;
}
export interface LegendObject extends Specification.Object {
    properties: LegendProperties;
}
export declare abstract class LegendClass extends ChartElementClass {
    readonly object: LegendObject;
    readonly state: LegendState;
    static metadata: ObjectClassMetadata;
    static defaultProperties: LegendProperties;
    attributeNames: string[];
    attributes: {
        [name: string]: AttributeDescription;
    };
    initializeState(): void;
    getLayoutBox(): {
        x1: number;
        y1: number;
        x2: number;
        y2: number;
    };
    getBoundingBox(): BoundingBox.Description;
    getHandles(): Handles.Description[];
    getScale(): [Specification.Scale, Specification.ScaleState];
    getLegendSize(): [number, number];
    private getOrderingObjects;
    getAttributePanelWidgets(manager: Prototypes.Controls.WidgetManager & CharticulatorPropertyAccessors): Controls.Widget[];
    getTemplateParameters(): TemplateParameters;
}
