import * as Graphics from "../../graphics";
import * as Specification from "../../specification";
import { AxisSide } from "../../specification/types";
import { ChartElementClass } from "../chart_element";
import { AttributeDescription, BoundingBox, Controls, Handles, ObjectClassMetadata } from "../common";
export declare enum NumericalNumberLegendAttributeNames {
    x1 = "x1",
    y1 = "y1",
    x2 = "x2",
    y2 = "y2",
    cx = "cx",
    cy = "cy",
    radius = "radius",
    startAngle = "startAngle",
    endAngle = "endAngle"
}
export interface NumericalNumberLegendAttributes extends Specification.AttributeMap {
    x1?: number;
    y1?: number;
    x2?: number;
    y2?: number;
    cx?: number;
    cy?: number;
    radius?: number;
    startAngle?: number;
    endAngle?: number;
}
interface NumericalNumberLegendAttributeDescription extends AttributeDescription {
    name: NumericalNumberLegendAttributeNames;
}
export interface NumericalNumberLegendProperties extends Specification.AttributeMap {
    axis: {
        visible: boolean;
        side: AxisSide;
        style: Specification.Types.AxisRenderingStyle;
        tickFormat: string;
    };
    polarAngularMode?: boolean;
}
export declare class NumericalNumberLegendClass extends ChartElementClass<NumericalNumberLegendProperties, NumericalNumberLegendAttributes> {
    static classID: string;
    static type: string;
    static metadata: ObjectClassMetadata;
    static defaultProperties: NumericalNumberLegendProperties;
    attributeNames: NumericalNumberLegendAttributeNames[];
    attributes: {
        [name in NumericalNumberLegendAttributeNames]: NumericalNumberLegendAttributeDescription;
    };
    initializeState(): void;
    getScale(): [Specification.Scale, Specification.ScaleState];
    getBoundingBox(): BoundingBox.Description;
    getHandles(): Handles.Description[];
    getGraphics(): Graphics.Element;
    private getPolarAxisGraphics;
    private getLineAxisGraphics;
    getGridLineGraphics(rangeMin: number, rangeMax: number, domainMin: number, domainMax: number): Graphics.Element;
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
}
export {};
