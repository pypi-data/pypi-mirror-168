import * as React from "react";
import { Dataset } from "../../../core";
import { AppStore } from "../../stores";
export interface FileUploaderProps {
    onChange: (file: File) => void;
    extensions: string[];
    filename?: string;
}
export interface FileUploaderState {
    filename: string;
    draggingOver: boolean;
}
export declare class FileUploader extends React.Component<FileUploaderProps, FileUploaderState> {
    private inputElement;
    constructor(props: FileUploaderProps);
    reset(): void;
    private onInputChange;
    private showOpenFile;
    private isDataTransferValid;
    private getFileFromDataTransfer;
    render(): JSX.Element;
}
export interface ImportDataViewProps {
    onConfirmImport?: (dataset: Dataset.Dataset) => void;
    onCancel?: () => void;
    showCancel?: boolean;
    store: AppStore;
}
export interface ImportDataViewState {
    dataTable: Dataset.Table;
    dataTableOrigin: Dataset.Table;
    imagesTable: Dataset.Table;
    linkTable: Dataset.Table;
    linkTableOrigin: Dataset.Table;
}
export declare class ImportDataView extends React.Component<ImportDataViewProps, ImportDataViewState> {
    state: {
        dataTable: Dataset.Table;
        imagesTable: Dataset.Table;
        linkTable: Dataset.Table;
        dataTableOrigin: Dataset.Table;
        linkTableOrigin: Dataset.Table;
    };
    private isComponentMounted;
    constructor(props: ImportDataViewProps);
    componentDidMount(): void;
    componentWillUnmount(): void;
    private loadFileAsTable;
    renderTable(table: Dataset.Table, onTypeChange: (column: string, type: Dataset.DataType) => void): JSX.Element;
    render(): JSX.Element;
    private checkSourceAndTargetColumns;
    private checkKeyColumn;
}
