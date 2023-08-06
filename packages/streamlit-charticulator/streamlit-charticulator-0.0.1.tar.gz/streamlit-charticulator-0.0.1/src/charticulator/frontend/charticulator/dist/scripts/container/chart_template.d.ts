import { Dataset, Specification } from "../core";
import { DefaultAttributes } from "../core/prototypes";
export interface TemplateInstance {
    chart: Specification.Chart;
    defaultAttributes: DefaultAttributes;
}
/** Represents a chart template */
export declare class ChartTemplate {
    private template;
    /**
     * Mapping of tables. Chart contains table and column names used in the designer app.
     * But data set can have column or table names with different names. It needs for expressions
     */
    private tableAssignment;
    /**
     * Mapping of columns. Chart contains table and column names used in the designer app.
     * But data set can have column or table names with different names It needs for expressions
     */
    private columnAssignment;
    /** Create a chart template */
    constructor(template: Specification.Template.ChartTemplate);
    getDatasetSchema(): Specification.Template.Table[];
    /** Reset slot assignments */
    reset(): void;
    /** Assign a table */
    assignTable(tableName: string, table: string): void;
    /** Assign an expression to a data mapping slot */
    assignColumn(tableName: string, columnName: string, column: string): void;
    /** Get variable map for a given table */
    getVariableMap(table: string): {};
    transformExpression(expr: string, table?: string): string;
    transformTextExpression(expr: string, table?: string): string;
    transformGroupBy(groupBy: Specification.Types.GroupBy, table: string): Specification.Types.GroupBy;
    /**
     * Creates instance of chart object from template. Chart objecty can be loaded into container to display it in canvas
     * On editing this method ensure that you made correspond changes in template builder ({@link ChartTemplateBuilder}).
     * Any exposed into template objects should be initialized here
     */
    instantiate(dataset: Dataset.Dataset, inference?: boolean): TemplateInstance;
    static SetChartProperty(chart: Specification.Chart, objectID: string, property: Specification.Template.PropertyField, value: Specification.AttributeValue): void;
    static GetChartProperty(chart: Specification.Chart, objectID: string, property: Specification.Template.PropertyField): Specification.AttributeValue;
    static SetChartAttributeMapping(chart: Specification.Chart, objectID: string, attribute: string, value: Specification.Mapping): void;
    static GetChartAttributeMapping(chart: Specification.Chart, objectID: string, attribute: string): any;
}
