import { Color } from "../../common";
import * as Specification from "../../specification";
import { Controls, ObjectClassMetadata } from "../common";
import { DataAxisExpression } from "../marks/data_axis.attrs";
import { LegendProperties, LegendState } from "./legend";
import { CategoricalLegendClass } from "./categorical_legend";
import { CharticulatorPropertyAccessors } from "../../../app/views/panels/widgets/types";
export declare type LegendSourceType = "columnNames" | "columnValues";
export declare type LegendType = "color" | "numerical" | "categorical";
export declare type LegendOrientation = "horizontal" | "vertical";
export interface CustomLegendProperties extends LegendProperties {
    legendType: LegendType;
    orientation: LegendOrientation;
    dataSource: LegendSourceType;
    dataExpressions: DataAxisExpression[];
    axis: {
        visible: boolean;
        side: string;
        style: Specification.Types.AxisRenderingStyle;
    };
}
export interface CustomLegendObject extends Specification.Object {
    properties: CustomLegendProperties;
}
export declare type CustomLegendState = LegendState;
export interface CustomLegendItem {
    type: "number" | "color" | "boolean";
    label: string;
    value: number | Color | boolean;
}
export declare class CustomLegendClass extends CategoricalLegendClass {
    static classID: string;
    static type: string;
    readonly object: CustomLegendObject;
    readonly state: CustomLegendState;
    static metadata: ObjectClassMetadata;
    getAttributePanelWidgets(manager: Controls.WidgetManager & CharticulatorPropertyAccessors): Controls.Widget[];
}
