import * as React from "react";
import { EventEmitter, EventSubscription } from "../../core";
export declare enum PopupAlignment {
    Inner = "inner",
    Outer = "outer",
    StartInner = "start-inner",
    StartOuter = "start-outer",
    EndInner = "end-inner",
    EndOuter = "end-outer"
}
export interface PopupOptions {
    parent?: PopupContext;
    anchor: Element;
    alignX?: PopupAlignment;
    alignY?: PopupAlignment;
}
export declare function getAlignment(anchor: Element): {
    alignLeft: boolean;
    alignX: PopupAlignment;
};
export declare class PopupContext extends EventEmitter {
    readonly id: string;
    element: JSX.Element;
    readonly options: PopupOptions;
    isClosed: boolean;
    parent: PopupContext;
    children: PopupContext[];
    constructor(id: string, renderElement: (context: PopupContext) => JSX.Element, options: PopupOptions);
    close(): void;
    traverse(visitor: (p: PopupContext) => void): void;
}
export declare class PopupController extends EventEmitter {
    private currentID;
    rootPopup: PopupContext;
    currentModal: PopupContext;
    traverse(visitor: (p: PopupContext) => void): void;
    popupAt(renderElement: (context: PopupContext) => JSX.Element, options: PopupOptions): void;
    showModal(renderElement: (context: PopupContext) => JSX.Element, options: PopupOptions): void;
    reset(): void;
    resetPopups(): void;
}
export interface PopupViewProps {
    controller: PopupController;
}
export declare class PopupContainer extends React.Component<PopupViewProps, Record<string, unknown>> {
    token: EventSubscription;
    private popupContainer;
    constructor(props: PopupViewProps);
    onKeyDown(e: KeyboardEvent): void;
    componentDidMount(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
    renderPopups(): JSX.Element;
}
interface PopupViewComponentProps {
    context: PopupContext;
    className?: string;
    width?: number;
}
export declare class PopupView extends React.Component<PopupViewComponentProps, Record<string, unknown>> {
    private popupContainer;
    componentDidMount(): void;
    render(): JSX.Element;
}
export declare class ModalView extends React.Component<{
    context: PopupContext;
    type?: string;
}, Record<string, unknown>> {
    render(): JSX.Element;
}
export {};
