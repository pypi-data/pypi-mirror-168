import { Color } from "../../common";
import * as Graphics from "../../graphics";
import { LegendClass, LegendProperties } from "./legend";
import { Controls } from "..";
import { CharticulatorPropertyAccessors } from "../../../app/views/panels/widgets/types";
export interface CategoricalLegendItem {
    type: "number" | "color" | "boolean";
    label: string;
    value: number | Color | boolean;
}
export declare const ReservedMappingKeyNamePrefix = "reserved_";
export declare class CategoricalLegendClass extends LegendClass {
    static classID: string;
    static type: string;
    static defaultProperties: LegendProperties;
    protected textMeasure: Graphics.TextMeasurer;
    getLegendItems(): CategoricalLegendItem[];
    getLineHeight(): number;
    getLineWidth(): number;
    getLegendSize(): [number, number];
    getGraphics(): Graphics.Element;
    getLayoutBox(): {
        x1: number;
        y1: number;
        x2: number;
        y2: number;
    };
    getAttributePanelWidgets(manager: Controls.WidgetManager & CharticulatorPropertyAccessors): Controls.Widget[];
}
