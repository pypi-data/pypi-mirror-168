import { Prototypes, Specification } from "../../../../core";
import { CharticulatorPropertyAccessors } from "./types";
interface EventListener {
    update(property: Prototypes.Controls.Property | Prototypes.Controls.Property[], value: Specification.AttributeValue): void;
}
export declare enum EventType {
    UPDATE_FIELD = 0
}
export declare class EventManager {
    private listeners;
    subscribe(type: EventType, listener: EventListener): void;
    notify(type: EventType, property: Prototypes.Controls.Property | Prototypes.Controls.Property[], value: Specification.AttributeValue): void;
}
export declare class UIManagerListener implements EventListener {
    private manager;
    constructor(manager: CharticulatorPropertyAccessors);
    update(property: Prototypes.Controls.Property, value: Specification.AttributeValue): void;
}
export {};
