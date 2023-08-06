import * as React from "react";
import { EventSubscription, Point, Prototypes, Specification } from "../../../../core";
import { DragData } from "../../../actions";
import { DragContext, DragModifiers, Droppable } from "../../../controllers/drag_controller";
import { AppStore } from "../../../stores";
export declare type OnEditMappingHandler = (attribute: string, mapping: Specification.Mapping) => void;
export declare type OnMapDataHandler = (attribute: string, data: DragData.DataExpression, hints: Prototypes.DataMappingHints) => void;
export declare type OnSetPropertyHandler = (property: string, field: string, value: Specification.AttributeValue) => void;
export interface CharticulatorPropertyAccessors {
    emitSetProperty?: (property: Prototypes.Controls.Property, value: Specification.AttributeValue) => void;
    store: AppStore;
    getAttributeMapping?: (attribute: string) => Specification.Mapping;
    onEditMappingHandler?: OnEditMappingHandler;
    onMapDataHandler?: OnMapDataHandler;
}
export interface DropZoneViewProps {
    /** Determine whether the data is acceptable */
    filter: (x: any) => boolean;
    /** The user dropped the thing */
    onDrop: (data: any, point: Point, modifiers: DragModifiers) => void;
    /** className of the root div element */
    className: string;
    onClick?: () => void;
    /** Display this instead when dragging (normally we show what's in this view) */
    draggingHint?: () => JSX.Element;
}
export interface DropZoneViewState {
    isInSession: boolean;
    isDraggingOver: boolean;
    data: any;
}
export declare class DropZoneView extends React.Component<DropZoneViewProps, DropZoneViewState> implements Droppable {
    dropContainer: HTMLDivElement;
    tokens: EventSubscription[];
    constructor(props: DropZoneViewProps);
    componentDidMount(): void;
    componentWillUnmount(): void;
    onDragEnter(ctx: DragContext): boolean;
    render(): JSX.Element;
}
export declare class ReorderStringsValue extends React.Component<{
    items: string[];
    onConfirm: (items: string[], customOrder: boolean) => void;
    allowReset?: boolean;
    onReset?: () => string[];
}, {
    items: string[];
    customOrder: boolean;
}> {
    state: {
        items: string[];
        customOrder: boolean;
    };
    render(): JSX.Element;
}
