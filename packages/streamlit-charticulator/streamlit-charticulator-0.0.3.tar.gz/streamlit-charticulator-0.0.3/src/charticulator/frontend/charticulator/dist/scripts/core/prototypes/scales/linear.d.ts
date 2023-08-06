import { ConstraintSolver, Variable } from "../../solver";
import * as Specification from "../../specification";
import { AttributeDescription, Controls, TemplateParameters, ObjectClassMetadata } from "../common";
import { ScaleClass } from "./index";
import { InferParametersOptions } from "./scale";
export interface LinearScaleProperties extends Specification.AttributeMap {
    domainMin: number;
    domainMax: number;
    autoDomainMin: boolean;
    autoDomainMax: boolean;
}
export interface LinearScaleAttributes extends Specification.AttributeMap {
    rangeMin: number;
    rangeMax: number;
}
export declare class LinearScale extends ScaleClass<LinearScaleProperties, LinearScaleAttributes> {
    static classID: string;
    static type: string;
    static defaultMappingValues: Specification.AttributeMap;
    static defaultProperties: Specification.AttributeMap;
    attributeNames: string[];
    attributes: {
        [name: string]: AttributeDescription;
    };
    mapDataToAttribute(data: Specification.DataValue): Specification.AttributeValue;
    buildConstraint(data: Specification.DataValue, target: Variable, solver: ConstraintSolver): void;
    initializeState(): void;
    inferParameters(column: Specification.DataValue[], options?: InferParametersOptions): void;
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
    getTemplateParameters(): TemplateParameters;
}
export interface LinearColorScaleProperties extends LinearScaleProperties {
    range: Specification.Types.ColorGradient;
}
export declare class LinearColorScale extends ScaleClass<LinearColorScaleProperties, any> {
    static classID: string;
    static type: string;
    static metadata: ObjectClassMetadata;
    static defaultMappingValues: Specification.AttributeMap;
    readonly object: {
        properties: LinearColorScaleProperties;
    } & Specification.Scale;
    attributeNames: string[];
    attributes: {
        [name: string]: AttributeDescription;
    };
    mapDataToAttribute(data: Specification.DataValue): Specification.AttributeValue;
    buildConstraint(data: Specification.DataValue, target: Variable, solver: ConstraintSolver): void;
    initializeState(): void;
    inferParameters(column: Specification.DataValue[], options?: InferParametersOptions): void;
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
    getTemplateParameters(): TemplateParameters;
}
export interface LinearBooleanScaleProperties extends LinearScaleProperties {
    min: number;
    max: number;
    mode: LinearBooleanScaleMode;
}
export declare enum LinearBooleanScaleMode {
    GreaterThan = "Greater than",
    LessThan = "Less than",
    Between = "Between",
    EqualTo = "Equal to",
    GreaterThanOrEqualTo = "Greater than or equal to",
    LessThanOrEqualTo = "Less than or equal to",
    NotBetween = "Not between",
    NotEqualTo = "Not Equal to"
}
export declare class LinearBooleanScale extends ScaleClass<LinearBooleanScaleProperties, any> {
    static classID: string;
    static type: string;
    static defaultMappingValues: Specification.AttributeMap;
    attributeNames: string[];
    attributes: {
        [name: string]: AttributeDescription;
    };
    mapDataToAttribute(data: Specification.DataValue): Specification.AttributeValue;
    buildConstraint(): void;
    initializeState(): void;
    inferParameters(column: Specification.DataValue[], options?: InferParametersOptions): void;
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
    getTemplateParameters(): TemplateParameters;
}
