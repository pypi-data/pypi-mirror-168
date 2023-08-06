/**
 * Components to save, open, create, export charts.
 *
 * ![File view](media://file_view.png)
 *
 * * {@link "app/views/file_view/new_view"} / {@link "app/views/file_view/import_data_view"} - component with two file inputs for main table data and links table data
 *
 * ![File view](media://file_view_new.png)
 *
 * * {@link "app/views/file_view/open_view"}
 *
 * ![File view](media://file_view_open.png)
 *
 * * {@link "app/views/file_view/save_view"}
 *
 * ![File view](media://file_view_save.png)
 *
 * * {@link "app/views/file_view/export_view"}
 *
 * ![File view](media://file_view_export.png)
 *
 * @packageDocumentation
 * @preferred
 */
import * as React from "react";
import { AbstractBackend } from "../../backend/abstract";
import { AppStore } from "../../stores";
export declare enum MainTabs {
    about = "about",
    export = "export",
    new = "new",
    open = "open",
    options = "options",
    save = "save"
}
export declare class CurrentChartView extends React.PureComponent<{
    store: AppStore;
}, {
    svgDataURL: string;
}> {
    constructor(props: {
        store: AppStore;
    });
    renderImage(): Promise<void>;
    render(): JSX.Element;
}
export interface FileViewProps {
    store: AppStore;
    backend: AbstractBackend;
    defaultTab?: MainTabs;
    onClose: () => void;
}
export interface FileViewState {
    currentTab: MainTabs;
}
export declare class FileView extends React.Component<FileViewProps, FileViewState> {
    refs: {
        inputSaveChartName: HTMLInputElement;
    };
    private buttonBack;
    constructor(props: FileViewProps);
    componentDidMount(): void;
    switchTab(currentTab: MainTabs): void;
    renderContent(): JSX.Element;
    render(): JSX.Element;
}
