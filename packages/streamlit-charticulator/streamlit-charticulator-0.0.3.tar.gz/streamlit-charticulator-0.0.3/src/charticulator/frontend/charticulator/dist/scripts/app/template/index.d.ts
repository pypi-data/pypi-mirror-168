/**
 * The {@link ChartTemplateBuilder} creates tempate ({@link ChartTemplate}) from the current chart.
 * {@link ChartTemplate} contains simplified version of {@link Chart} object in {@link ChartTemplate.specification} property.
 * Tempate can be exported as *.tmplt file (JSON format). It also uses on export to HTML file or on export as Power BI visual.
 *
 * Template can be loaded into container outside of Charticulator app to visualize with custom dataset.
 *
 * @packageDocumentation
 * @preferred
 */
import { Dataset, Prototypes, Specification } from "../../core";
export interface ExportTemplateTargetProperty {
    displayName: string;
    name: string;
    type: string;
    default: any;
}
/** Represents target chart template export format */
export interface ExportTemplateTarget {
    /** Get export format properties, such as template name, author */
    getProperties(): ExportTemplateTargetProperty[];
    /** Get the file name of the exported artifact */
    getFileName?(properties: {
        [name: string]: any;
    }): string;
    /** Deprecated: get the file extension of the exported artifact */
    getFileExtension?(properties: {
        [name: string]: any;
    }): string;
    /** Generate the exported template, return a base64 string encoding the file */
    generate(properties: {
        [name: string]: any;
    }): Promise<string>;
}
/** Class builds the template from given {@link Specification.Chart} object  */
export declare class ChartTemplateBuilder {
    readonly chart: Specification.Chart;
    readonly dataset: Dataset.Dataset;
    readonly manager: Prototypes.ChartStateManager;
    readonly version: string;
    protected template: Specification.Template.ChartTemplate;
    protected tableColumns: {
        [name: string]: Set<string>;
    };
    private objectVisited;
    constructor(chart: Specification.Chart, dataset: Dataset.Dataset, manager: Prototypes.ChartStateManager, version: string);
    reset(): void;
    addTable(table: string): void;
    addColumn(table: string, columnName: string): void;
    addColumnsFromExpression(table: string, expr: string, textExpression?: boolean): void;
    propertyToString(property: Specification.Template.PropertyField): string;
    addObject(table: string, objectClass: Prototypes.ObjectClass): void;
    /**
     * Builds template.
     * All exposed objects should be initialized in {@link ChartTemplate} class
     * @returns JSON structure of template
     */
    build(): Specification.Template.ChartTemplate;
    private usedColumns;
    private trackColumnFromExpression;
    trackTable(table: string): {
        [name: string]: string;
    };
    /**
     * Computes the default attributes
     */
    private computeDefaultAttributes;
}
