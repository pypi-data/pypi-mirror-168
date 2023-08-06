/**
 * See {@link DatasetView} or {@link TableView}
 * @packageDocumentation
 * @preferred
 */
import * as React from "react";
import { Dataset } from "../../../core";
import { AppStore } from "../../stores";
import { DataType, DataKind } from "../../../core/specification";
export interface DatasetViewProps {
    store: AppStore;
}
/**
 * Component for displaying dataset on the left side of app
 *
 * ![Mark widgets](media://dataset_view.png)
 */
export declare class DatasetView extends React.Component<DatasetViewProps, Record<string, unknown>> {
    componentDidMount(): void;
    render(): JSX.Element;
    onImportConnections(): void;
}
export interface ColumnsViewProps {
    store: AppStore;
    table: Dataset.Table;
}
export interface ColumnsViewState {
    selectedColumn: string;
    tableViewIsOpened: boolean;
}
export declare class ColumnsView extends React.Component<ColumnsViewProps, ColumnsViewState> {
    private popupController;
    constructor(props: ColumnsViewProps);
    render(): JSX.Element;
}
export declare class ColumnViewProps {
    store: AppStore;
    table: Dataset.Table;
    column: Dataset.Column;
}
export declare class ColumnViewState {
    isSelected: string;
    isExpanded: boolean;
}
export declare class ColumnView extends React.Component<ColumnViewProps, ColumnViewState> {
    private columnRef;
    constructor(props: ColumnViewProps);
    renderDerivedColumns(): JSX.Element;
    applyAggregation(expr: string, type: DataType, kind: DataKind): string;
    renderColumnControl(label: string, icon: string, expr: string, lambdaExpr: string, type: Dataset.DataType, additionalElement: JSX.Element, metadata: Dataset.ColumnMetadata, onColumnKindChanged?: (column: string, type: string) => void, rawColumnExpr?: string, displayLabel?: string): JSX.Element;
    render(): JSX.Element;
}
