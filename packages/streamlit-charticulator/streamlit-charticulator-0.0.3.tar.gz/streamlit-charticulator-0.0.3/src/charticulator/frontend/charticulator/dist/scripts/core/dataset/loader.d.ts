import { Table, Dataset } from "./dataset";
import { LocaleFileFormat } from "./dsv_parser";
export interface TableSourceSpecification {
    /** Name of the table, if empty, use the basename of the url without extension */
    name?: string;
    /** Locale-based delimiter and number format */
    localeFileFormat: LocaleFileFormat;
    /** Option 1: Specify the url to load the table from */
    url?: string;
    /** Option 2: Specify the table content, in this case format and name must be specified */
    content?: string;
}
export interface DatasetSourceSpecification {
    name?: string;
    tables: TableSourceSpecification[];
}
export declare class DatasetLoader {
    loadTextData(url: string): Promise<string>;
    loadDSVFromURL(url: string, localeFileFormat: LocaleFileFormat): Promise<Table>;
    loadDSVFromContents(filename: string, contents: string, localeFileFormat: LocaleFileFormat): Table;
    loadTableFromSourceSpecification(spec: TableSourceSpecification): Promise<Table>;
    loadDatasetFromSourceSpecification(spec: DatasetSourceSpecification): Promise<Dataset>;
}
