import { Specification, Prototypes } from "../../../../core";
import { Actions } from "../../../actions";
import { SnappingAction, SnappableGuide } from "./common";
import { SnappingSession } from "./session";
export declare type MarkSnappableGuide = SnappableGuide<Specification.Element>;
export declare class MarkSnappingSession extends SnappingSession<Specification.Element> {
    mark: Specification.Glyph;
    element: Specification.Element;
    constructor(guides: SnappableGuide<Specification.Element>[], mark: Specification.Glyph, element: Specification.Element, elementState: Specification.MarkState, bound: Prototypes.Handles.Description, threshold: number, findClosestSnappingGuide: boolean);
    getActions(actions: SnappingAction<Specification.Element>[]): Actions.Action;
}
