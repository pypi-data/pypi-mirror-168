import { Point } from "../../common";
import * as Graphics from "../../graphics";
import * as Specification from "../../specification";
import { BoundingBox, Controls, DropZones, Handles, LinkAnchor, ObjectClassMetadata, SnappingGuides, TemplateParameters } from "../common";
import { ChartStateManager } from "../state";
import { EmphasizableMarkClass } from "./emphasis";
import { IconElementAttributes, IconElementProperties } from "./icon.attrs";
export { IconElementAttributes, IconElementProperties };
export declare class IconElementClass extends EmphasizableMarkClass<IconElementProperties, IconElementAttributes> {
    static classID: string;
    static type: string;
    static metadata: ObjectClassMetadata;
    static defaultProperties: Partial<IconElementProperties>;
    static defaultMappingValues: Partial<IconElementAttributes>;
    attributes: import("../object").AttributeDescriptions;
    attributeNames: string[];
    initializeState(): void;
    /** Get link anchors for this mark */
    getLinkAnchors(mode: "begin" | "end"): LinkAnchor.Description[];
    getLayoutProps(): {
        width: number;
        height: number;
        dx: number;
        dy: number;
    };
    getCenterOffset(alignment: Specification.Types.TextAlignment, width: number, height: number): [number, number];
    /** Get the graphical element from the element */
    getGraphics(cs: Graphics.CoordinateSystem, offset: Point, glyphIndex: number, manager: ChartStateManager, emphasize?: boolean): Graphics.Element;
    /** Get DropZones given current state */
    getDropZones(): DropZones.Description[];
    /** Get bounding rectangle given current state */
    getHandles(): Handles.Description[];
    getBoundingRectangle(): {
        cx: number;
        cy: number;
        width: number;
        height: number;
        rotation: number;
    };
    getBoundingBox(): BoundingBox.Description;
    getSnappingGuides(): SnappingGuides.Description[];
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
    getTemplateParameters(): TemplateParameters;
}
