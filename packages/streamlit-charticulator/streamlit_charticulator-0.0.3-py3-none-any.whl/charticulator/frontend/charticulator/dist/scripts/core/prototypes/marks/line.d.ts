import { Point } from "../../common";
import { ConstraintSolver } from "../../solver";
import { LineElementAttributes, LineElementProperties } from "./line.attrs";
import { BoundingBox, Controls, DropZones, Handles, LinkAnchor, ObjectClassMetadata, SnappingGuides, TemplateParameters } from "../common";
import * as Graphics from "../../graphics";
import { EmphasizableMarkClass } from "./emphasis";
import { ChartStateManager } from "../state";
export { LineElementAttributes, LineElementProperties };
export declare class LineElementClass extends EmphasizableMarkClass<LineElementProperties, LineElementAttributes> {
    static classID: string;
    static type: string;
    static metadata: ObjectClassMetadata;
    static defaultProperties: Partial<LineElementProperties>;
    static defaultMappingValues: Partial<LineElementAttributes>;
    attributes: import("../object").AttributeDescriptions;
    attributeNames: string[];
    initializeState(): void;
    /** Get link anchors for this mark */
    getLinkAnchors(mode: "begin" | "end"): LinkAnchor.Description[];
    /** Get intrinsic constraints between attributes (e.g., x2 - x1 = width for rectangles) */
    buildConstraints(solver: ConstraintSolver): void;
    /** Get the graphical element from the element */
    getGraphics(cs: Graphics.CoordinateSystem, offset: Point, glyphIndex: number, manager: ChartStateManager, emphasize?: boolean): Graphics.Element;
    /** Get DropZones given current state */
    getDropZones(): DropZones.Description[];
    /** Get bounding rectangle given current state */
    getHandles(): Handles.Description[];
    getBoundingBox(): BoundingBox.Description;
    getSnappingGuides(): SnappingGuides.Description[];
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
    getTemplateParameters(): TemplateParameters;
}
