import { Color } from "../../common";
import { ConstraintSolver, Variable } from "../../solver";
import { DataValue, AttributeValue, AttributeMap } from "../../specification";
import { AttributeDescription, Controls, ObjectClassMetadata } from "../common";
import { ScaleClass } from "./index";
import { AttributeDescriptions } from "../object";
import { InferParametersOptions } from "./scale";
import { Specification } from "../..";
export interface CategoricalScaleProperties<ValueType extends AttributeValue> extends AttributeMap {
    mapping: {
        [name: string]: ValueType;
    };
    defaultRange?: ValueType[];
}
export interface CategoricalScaleNumberAttributes extends AttributeMap {
    rangeScale?: number;
}
export declare class CategoricalScaleNumber extends ScaleClass<CategoricalScaleProperties<number>, CategoricalScaleNumberAttributes> {
    static classID: string;
    static type: string;
    attributeNames: string[];
    attributes: {
        [name: string]: AttributeDescription;
    };
    static defaultProperties: Specification.AttributeMap;
    mapDataToAttribute(data: DataValue): AttributeValue;
    buildConstraint(data: DataValue, target: Variable, solver: ConstraintSolver): void;
    initializeState(): void;
    inferParameters(column: DataValue[], options?: InferParametersOptions): void;
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
}
export declare class CategoricalScaleColor extends ScaleClass<CategoricalScaleProperties<Color>, any> {
    static metadata: ObjectClassMetadata;
    static classID: string;
    static type: string;
    attributeNames: string[];
    attributes: AttributeDescriptions;
    mapDataToAttribute(data: DataValue): AttributeValue;
    initializeState(): void;
    inferParameters(column: DataValue[], options?: InferParametersOptions): void;
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
}
export declare class CategoricalScaleEnum extends ScaleClass<CategoricalScaleProperties<string>, any> {
    static classID: string;
    static type: string;
    attributeNames: string[];
    attributes: {
        [name: string]: AttributeDescription;
    };
    mapDataToAttribute(data: DataValue): AttributeValue;
    initializeState(): void;
    inferParameters(column: DataValue[], options?: InferParametersOptions): void;
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
}
export declare class CategoricalScaleBoolean extends ScaleClass<CategoricalScaleProperties<boolean>, any> {
    static classID: string;
    static type: string;
    attributeNames: string[];
    attributes: {
        [name: string]: AttributeDescription;
    };
    mapDataToAttribute(data: DataValue): AttributeValue;
    initializeState(): void;
    inferParameters(column: DataValue[], options?: InferParametersOptions): void;
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
}
export declare class CategoricalScaleImage extends ScaleClass<CategoricalScaleProperties<string>, any> {
    static classID: string;
    static type: string;
    attributeNames: string[];
    attributes: {
        [name: string]: AttributeDescription;
    };
    mapDataToAttribute(data: DataValue): AttributeValue;
    initializeState(): void;
    inferParameters(column: DataValue[], options?: InferParametersOptions): void;
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
}
export declare class CategoricalScaleBase64Image extends ScaleClass<CategoricalScaleProperties<string>, any> {
    static classID: string;
    static type: string;
    attributeNames: string[];
    attributes: {
        [name: string]: AttributeDescription;
    };
    mapDataToAttribute(data: DataValue): AttributeValue;
    initializeState(): void;
    inferParameters(idColumn: string[], options: InferParametersOptions): void;
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
}
