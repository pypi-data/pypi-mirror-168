import { Prototypes } from "../../../../core";
import { HandlesDragEvent } from "../handles/common";
import { SnappableGuide, SnappingAction } from "./common";
export declare class SnappingSession<ElementType> {
    candidates: SnappableGuide<ElementType>[];
    handle: Prototypes.Handles.Description;
    threshold: number;
    findClosestSnappingGuide: boolean;
    currentCandidates: SnappableGuide<ElementType>[];
    constructor(guides: SnappableGuide<ElementType>[], handle: Prototypes.Handles.Description, threshold: number, findClosest: boolean);
    private giveProrityToPoint;
    handleDrag(e: HandlesDragEvent): void;
    handleEnd(e: HandlesDragEvent): SnappingAction<ElementType>[];
    getCurrentCandidates(): SnappableGuide<ElementType>[];
}
