import { Dataset, Specification } from "../../core";
/** Create a default glyph */
export declare function createDefaultGlyph(tableName: string): Specification.Glyph<Specification.ObjectProperties>;
/** Create a default plot segment */
export declare function createDefaultPlotSegment(table: Dataset.Table, glyph: Specification.Glyph): Specification.PlotSegment<Specification.ObjectProperties>;
/** Create a default chart title */
export declare function createDefaultTitle(dataset: Dataset.Dataset): Specification.ChartElement<Specification.ObjectProperties>;
/** Create a default chart */
export declare function createDefaultChart(dataset: Dataset.Dataset, createTitle: boolean): Specification.Chart<Specification.ObjectProperties>;
export declare const defaultFont = "Segoe UI";
export declare const defaultFontSize = 12;
export declare const defaultFontSizeLegend = 12;
export declare const defaultVersionOfTemplate = "2.0.3";
