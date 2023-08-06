/**
 * See {@link DatasetView} or {@link TableView}
 * @packageDocumentation
 * @preferred
 */
import * as React from "react";
import { Dataset } from "../../../core";
export interface TableViewProps {
    table: Dataset.Table;
    maxRows?: number;
    onTypeChange?: (column: string, type: string) => void;
}
/**
 * Component for displaying data samples on loading or in context menu of {@link DatasetView}
 *
 * ![Table view](media://table_view.png)
 *
 * ![Table view](media://table_view_leftside.png)
 */
export declare class TableView extends React.Component<TableViewProps, any> {
    render(): JSX.Element;
}
