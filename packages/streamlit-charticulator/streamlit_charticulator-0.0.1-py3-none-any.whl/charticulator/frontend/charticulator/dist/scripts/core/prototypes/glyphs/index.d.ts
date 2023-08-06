/**
 * ![Chart levels](media://glyph-levels.png)
 *
 * The Chart-level specification includes chart elements, layout constraints between them, and scales. The most important chart element is
 * a plot segment, which lays out glyphs according to its scaffolds and/or
 * axes, and transforms them according to its coordinate system, scales specify how data is mapped to attributes
 * such as width, height, and color, and they can be shared among several
 * marks. Legends visualize the scales used in the chart.
 *
 * @packageDocumentation
 * @preferred
 */
import * as Specification from "../../specification";
import { ConstraintSolver } from "../../solver";
import { AttributeDescription, Controls, Handles, ObjectClass, ObjectClassMetadata, SnappingGuides } from "../common";
export declare abstract class GlyphClass extends ObjectClass {
    readonly object: Specification.Glyph;
    readonly state: Specification.GlyphState;
    static metadata: ObjectClassMetadata;
    abstract initializeState(): void;
    abstract buildIntrinsicConstraints(solver: ConstraintSolver): void;
    abstract getAlignmentGuides(): SnappingGuides.Description[];
    abstract getHandles(): Handles.Description[];
    static createDefault(table: string): Specification.Glyph;
}
export interface RectangleGlyphAttributes extends Specification.AttributeMap {
    x1: number;
    y1: number;
    x2: number;
    y2: number;
    x: number;
    y: number;
    width: number;
    height: number;
    ix1: number;
    iy1: number;
    ix2: number;
    iy2: number;
    icx: number;
    icy: number;
}
export interface RectangleGlyphState extends Specification.GlyphState {
    attributes: RectangleGlyphAttributes;
}
export declare class RectangleGlyph extends GlyphClass {
    static classID: string;
    static type: string;
    readonly state: RectangleGlyphState;
    attributeNames: string[];
    attributes: {
        [name: string]: AttributeDescription;
    };
    initializeState(): void;
    buildIntrinsicConstraints(solver: ConstraintSolver): void;
    getAlignmentGuides(): SnappingGuides.Description[];
    getHandles(): Handles.Description[];
    getAttributePanelWidgets(manager: Controls.WidgetManager): Controls.Widget[];
}
export declare function registerClasses(): void;
