import * as React from "react";
import { Specification } from "../../../core";
import { AppStore } from "../../stores";
import { ExportTemplateTarget } from "../../template";
export declare class InputGroup extends React.Component<{
    value: string;
    label: string;
    onChange: (newValue: string) => void;
}, Record<string, unknown>> {
    private ref;
    render(): JSX.Element;
}
export declare class ExportImageView extends React.Component<{
    store: AppStore;
}, {
    dpi: string;
}> {
    state: {
        dpi: string;
    };
    getScaler(): number;
    render(): JSX.Element;
}
export declare class ExportHTMLView extends React.Component<{
    store: AppStore;
}, Record<string, unknown>> {
    render(): JSX.Element;
}
export interface FileViewExportState {
    exportMode: string;
}
export declare class FileViewExport extends React.Component<{
    onClose: () => void;
    store: AppStore;
}, FileViewExportState> {
    state: FileViewExportState;
    renderExportView(mode: "image" | "html"): JSX.Element;
    renderExportTemplate(): JSX.Element;
    render(): JSX.Element;
}
export interface ExportTemplateViewState {
    template: Specification.Template.ChartTemplate;
    target: ExportTemplateTarget;
    targetProperties: {
        [name: string]: string;
    };
}
export declare class ExportTemplateView extends React.Component<{
    exportKind: string;
    store: AppStore;
}, ExportTemplateViewState> {
    state: ExportTemplateViewState;
    getDefaultState(kind: string): ExportTemplateViewState;
    componentWillReceiveProps(newProps: {
        exportKind: string;
    }): void;
    /** Renders input fields for extension properties */
    renderInput(label: string, type: string, value: any, defaultValue: any, onChange: (value: any) => void): JSX.Element;
    /** Renders all fields for extension properties */
    renderTargetProperties(): JSX.Element[];
    /** Renders column names for export view */
    renderSlots(): JSX.Element | JSX.Element[];
    private getOriginalColumn;
    renderInferences(): JSX.Element | JSX.Element[];
    /** Renders object/properties list of chart */
    renderExposedProperties(): JSX.Element[];
    render(): JSX.Element;
}
