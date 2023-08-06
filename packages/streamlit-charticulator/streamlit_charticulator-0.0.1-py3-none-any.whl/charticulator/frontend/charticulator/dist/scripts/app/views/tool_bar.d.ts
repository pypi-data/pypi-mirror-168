import * as React from "react";
import { EventSubscription } from "../../core";
import { ContextedComponent } from "../context_component";
import { LayoutDirection, UndoRedoLocation } from "../main_view";
export declare class Toolbar extends ContextedComponent<{
    layout: LayoutDirection;
    undoRedoLocation: UndoRedoLocation;
    toolbarLabels: boolean;
}, {
    innerWidth: number;
}> {
    token: EventSubscription;
    state: {
        innerWidth: number;
    };
    private resizeListener;
    componentDidMount(): void;
    componentWillUnmount(): void;
    private renderGuidesButton;
    private renderPlotSegmentsButton;
    private renderMarksButton;
    private renderSymbolButton;
    private renderLineButton;
    private renderTextButton;
    private renderIconButton;
    private renderDataAxisButton;
    private renderScaffoldButton;
    private getGlyphToolItems;
    private getChartToolItems;
    private getToolItems;
    render(): JSX.Element;
}
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
}> {
    state: {
        currentSelection: {
            classID: string;
            options: string;
        };
    };
    private refButton;
    token: EventSubscription;
    isActive(): boolean;
    getSelectedTool(): ObjectButtonProps;
    componentDidMount(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
}
export declare class ScaffoldButton extends ContextedComponent<{
    currentTool: string;
    title: string;
    type: string;
    icon: string;
}, Record<string, unknown>> {
    render(): JSX.Element;
}
export declare class LinkButton extends ContextedComponent<{
    label: boolean;
}, Record<string, unknown>> {
    container: HTMLSpanElement;
    render(): JSX.Element;
}
export declare class LegendButton extends ContextedComponent<Record<string, unknown>, Record<string, unknown>> {
    container: HTMLSpanElement;
    render(): JSX.Element;
}
export declare class CheckboxButton extends React.Component<{
    value: boolean;
    text?: string;
    onChange?: (v: boolean) => void;
}, Record<string, unknown>> {
    render(): JSX.Element;
}
