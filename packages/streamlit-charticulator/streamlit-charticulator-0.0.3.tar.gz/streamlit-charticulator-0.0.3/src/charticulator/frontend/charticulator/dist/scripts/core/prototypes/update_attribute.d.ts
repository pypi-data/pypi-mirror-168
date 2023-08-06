import { AttributeValue, Constraint } from "../specification";
import { ChartStateManager } from "./state";
export declare function onUpdateAttribute(manager: ChartStateManager, elementID: string, attribute: string, value: AttributeValue): void;
export declare function snapToAttribute(manager: ChartStateManager, chartConstraints: Constraint[], objectId: string, attrName: string, attrValue: AttributeValue): void;
