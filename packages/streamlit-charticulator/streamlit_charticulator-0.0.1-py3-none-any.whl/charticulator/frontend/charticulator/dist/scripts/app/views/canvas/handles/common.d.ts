import { EventEmitter } from "../../../../core";
import { Specification, Prototypes, ZoomInfo } from "../../../../core";
export interface HandlesDragEvent {
    [name: string]: Specification.AttributeValue;
}
export declare class HandlesDragContext extends EventEmitter {
    onDrag(listener: (e: HandlesDragEvent) => void): import("../../../../core").EventSubscription;
    onEnd(listener: (e: HandlesDragEvent) => void): import("../../../../core").EventSubscription;
}
export interface HandleViewProps {
    zoom: ZoomInfo;
    active?: boolean;
    visible?: boolean;
    snapped?: boolean;
    onDragStart?: (handle: Prototypes.Handles.Description, ctx: HandlesDragContext) => void;
}
