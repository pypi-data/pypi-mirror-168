import { Specification, Prototypes } from "../../../../core";
import { SnappingAction } from "./common";
import { SnappingSession } from "./session";
export declare class MoveSnappingSession extends SnappingSession<void> {
    constructor(handle: Prototypes.Handles.Description);
    getUpdates(actions: SnappingAction<void>[]): {
        [name: string]: Specification.AttributeValue;
    };
}
