import * as Graphics from "../../graphics";
import { LegendClass, LegendProperties } from "./legend";
import { Controls } from "../common";
import { CharticulatorPropertyAccessors } from "../../../app/views/panels/widgets/types";
export declare class NumericalColorLegendClass extends LegendClass {
    static classID: string;
    static type: string;
    static defaultLegendLength: number;
    static defaultProperties: LegendProperties;
    private gradientWidth;
    getLineHeight(): number;
    getLegendSize(): [number, number];
    private isHorizontalOrientation;
    getGraphics(): Graphics.Element;
    getAttributePanelWidgets(manager: Controls.WidgetManager & CharticulatorPropertyAccessors): Controls.Widget[];
}
