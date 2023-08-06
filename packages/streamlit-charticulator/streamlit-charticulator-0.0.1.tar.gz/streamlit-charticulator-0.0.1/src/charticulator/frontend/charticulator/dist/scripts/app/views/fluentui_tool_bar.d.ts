import * as React from "react";
import { EventSubscription } from "../../core";
import { ContextedComponent } from "../context_component";
import { LayoutDirection, UndoRedoLocation } from "../main_view";
export declare const FluentUIToolbar: React.FC<{
    layout: LayoutDirection;
    undoRedoLocation: UndoRedoLocation;
    toolbarLabels: boolean;
}>;
export interface ObjectButtonProps {
    title: string;
    text?: string;
    classID: string;
    icon: string;
    options?: string;
    noDragging?: boolean;
    onClick?: () => void;
    onDrag?: () => any;
    compact?: boolean;
}
export declare class ObjectButton extends ContextedComponent<ObjectButtonProps, Record<string, unknown>> {
    token: EventSubscription;
    getIsActive(): boolean;
    componentDidMount(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
}
export declare class MultiObjectButton extends ContextedComponent<{
    compact?: boolean;
    tools: ObjectButtonProps[];
}, {
    currentSelection: {
        classID: string;
        options: string;
    };
    dragging: boolean;
}> {
    state: {
        currentSelection: {
            classID: string;
            options: string;
        };
        dragging: boolean;
    };
    token: EventSubscription;
    isActive(): boolean;
    getSelectedTool(): ObjectButtonProps;
    componentDidMount(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
}
export declare const ScaffoldButton: React.FC<{
    currentTool: string;
    title: string;
    type: string;
    icon: string;
}>;
export declare const LinkButton: React.FC<{
    label: boolean;
}>;
export declare const LegendButton: React.FC;
export declare class CheckboxButton extends React.Component<{
    value: boolean;
    text?: string;
    onChange?: (v: boolean) => void;
}, Record<string, unknown>> {
    render(): JSX.Element;
}
