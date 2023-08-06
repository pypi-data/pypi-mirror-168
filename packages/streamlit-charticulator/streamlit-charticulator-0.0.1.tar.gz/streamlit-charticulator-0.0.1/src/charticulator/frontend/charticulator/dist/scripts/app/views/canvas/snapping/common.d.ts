import { Specification, Prototypes } from "../../../../core";
export interface SnappableGuide<ElementType> {
    element: ElementType;
    guide: Prototypes.SnappingGuides.Description;
}
export interface SnappingAction<ElementType> {
    type: "snap" | "move" | "property" | "value-mapping";
    attribute?: string;
    property?: string;
    field?: string | string[];
    value?: Specification.AttributeValue;
    snapElement?: ElementType;
    snapAttribute?: string;
}
