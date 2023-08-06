import * as Specification from "../../specification";
import { AttributeDescription, Controls, Handles, ObjectClassMetadata } from "../common";
import { MarkClass } from "./mark";
export interface AnchorElementAttributes extends Specification.AttributeMap {
    x: number;
    y: number;
}
export interface AnchorElementState extends Specification.MarkState {
    attributes: AnchorElementAttributes;
}
export declare class AnchorElement extends MarkClass {
    static classID: string;
    static type: string;
    static metadata: ObjectClassMetadata;
    readonly state: AnchorElementState;
    /** Get a list of elemnt attributes */
    attributeNames: string[];
    attributes: {
        [name: string]: AttributeDescription;
    };
    /** Initialize the state of an element so that everything has a valid value */
    initializeState(): void;
    /** Get bounding rectangle given current state */
    getHandles(): Handles.Description[];
    static createDefault(glyph: Specification.Glyph): Specification.Element;
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
}
