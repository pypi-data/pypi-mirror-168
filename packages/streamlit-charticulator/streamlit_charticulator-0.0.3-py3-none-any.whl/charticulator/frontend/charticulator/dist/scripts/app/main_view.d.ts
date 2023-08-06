import * as React from "react";
import { TelemetryRecorder } from "./components";
import { AppStore } from "./stores";
import { MenuBar, MenuBarHandlers, MenubarTabButton } from "./views/menubar";
export declare enum UndoRedoLocation {
    MenuBar = "menubar",
    ToolBar = "toolbar"
}
export declare enum PositionsLeftRight {
    Left = "left",
    Right = "right"
}
export declare enum PositionsLeftRightTop {
    Left = "left",
    Right = "right",
    Top = "top"
}
export declare enum LayoutDirection {
    Vertical = "vertical",
    Horizontal = "horizontal"
}
export interface MainViewConfig {
    ColumnsPosition: PositionsLeftRight;
    EditorPanelsPosition: PositionsLeftRight;
    ToolbarPosition: PositionsLeftRightTop;
    MenuBarButtons: PositionsLeftRight;
    MenuBarSaveButtons: PositionsLeftRight;
    Name?: string;
    ToolbarLabels: boolean;
    UndoRedoLocation: UndoRedoLocation;
}
export interface MainViewProps {
    store: AppStore;
    viewConfiguration: MainViewConfig;
    menuBarHandlers?: MenuBarHandlers;
    telemetry?: TelemetryRecorder;
    tabButtons?: MenubarTabButton[];
}
export interface MainViewState {
    glyphViewMaximized: boolean;
    layersViewMaximized: boolean;
    attributeViewMaximized: boolean;
    scaleViewMaximized: boolean;
    currentFocusComponentIndex: number;
}
export declare class MainView extends React.Component<MainViewProps, MainViewState> {
    refMenuBar: MenuBar;
    private viewConfiguration;
    constructor(props: MainViewProps);
    private shortcutKeyHandler;
    componentDidMount(): void;
    getFocusableComponents(): NodeListOf<HTMLElement>;
    componentWillUnmount(): void;
    static childContextTypes: {
        store: (s: AppStore) => boolean;
    };
    getChildContext(): {
        store: AppStore;
    };
    render(): JSX.Element;
}
