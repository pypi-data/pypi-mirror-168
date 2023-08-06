import * as React from "react";
import { EventSubscription } from "../../core";
import { ContextedComponent, MainContextInterface } from "../context_component";
import { MainTabs } from "./file_view";
import { PositionsLeftRight, UndoRedoLocation } from "../main_view";
interface HelpButtonProps {
    hideReportIssues: boolean;
    handlers: MenuBarHandlers;
}
export declare class HelpButton extends React.Component<HelpButtonProps, Record<string, unknown>> {
    render(): JSX.Element;
}
export interface MenuBarHandlers {
    onContactUsLink?: () => void;
    onImportTemplateClick?: () => void;
    onExportTemplateClick?: () => void;
    onCopyToClipboardClick?: () => void;
}
export interface MenubarTabButton {
    icon: string;
    tooltip: string;
    text: string;
    active: boolean;
    onClick: () => void;
}
export interface MenuBarProps {
    undoRedoLocation: UndoRedoLocation;
    alignButtons: PositionsLeftRight;
    alignSaveButton: PositionsLeftRight;
    name?: string;
    handlers: MenuBarHandlers;
    tabButtons?: MenubarTabButton[];
}
export declare class MenuBar extends ContextedComponent<MenuBarProps, {
    showSaveDialog: boolean;
}> {
    protected editor: EventSubscription;
    protected graphics: EventSubscription;
    private popupController;
    constructor(props: MenuBarProps, context: MainContextInterface);
    componentDidMount(): void;
    componentWillUnmount(): void;
    keyboardMap: {
        [name: string]: string;
    };
    onKeyDown: (e: KeyboardEvent) => void;
    hideFileModalWindow(): void;
    showFileModalWindow(defaultTab?: MainTabs): void;
    renderSaveNested(): JSX.Element;
    renderImportButton(props: MenuBarProps): JSX.Element;
    renderExportButton(props: MenuBarProps): JSX.Element;
    renderCopyToClipboard(props: MenuBarProps): JSX.Element;
    renderSaveEmbedded(): JSX.Element;
    renderDelete(): JSX.Element;
    renderNewOpenSave(): JSX.Element;
    toolbarButtons(props: MenuBarProps): JSX.Element;
    toolbarTabButtons(props: MenuBarProps): JSX.Element;
    render(): JSX.Element;
}
export {};
