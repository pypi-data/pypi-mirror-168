import { Specification, Prototypes } from "../../../../core";
import { Actions } from "../../../actions";
import { SnappingAction, SnappableGuide } from "./common";
import { SnappingSession } from "./session";
export declare type ChartSnappableGuide = SnappableGuide<Specification.ChartElement>;
export declare class ChartSnappingSession extends SnappingSession<Specification.ChartElement> {
    markLayout: Specification.ChartElement;
    constructor(guides: SnappableGuide<Specification.ChartElement>[], markLayout: Specification.ChartElement, bound: Prototypes.Handles.Description, threshold: number, findClosestSnappingGuide: boolean);
    getActions(actions: SnappingAction<Specification.ChartElement>[]): Actions.Action[];
}
