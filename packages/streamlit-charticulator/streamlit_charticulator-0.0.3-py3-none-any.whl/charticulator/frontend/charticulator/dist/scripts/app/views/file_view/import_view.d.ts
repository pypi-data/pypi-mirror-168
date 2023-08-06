/// <reference types="react" />
import { ContextedComponent } from "../../context_component";
import { Specification } from "../../../core";
import { Table } from "../../../core/dataset/dataset";
export declare enum MappingMode {
    ImportTemplate = 0,
    ImportDataset = 1
}
export interface FileViewImportProps {
    mode: MappingMode;
    tables: Specification.Template.Table[];
    datasetTables: Table[];
    tableMapping: Map<string, string>;
    unmappedColumns: Specification.Template.Column[];
    onSave: (columnMapping: Map<string, string>) => void;
    onClose: () => void;
}
export interface FileViewImportState {
    saving?: boolean;
    error?: string;
    columnMappings: Map<string, string>;
}
export declare class FileViewImport extends ContextedComponent<FileViewImportProps, FileViewImportState> {
    state: FileViewImportState;
    render(): JSX.Element;
}
