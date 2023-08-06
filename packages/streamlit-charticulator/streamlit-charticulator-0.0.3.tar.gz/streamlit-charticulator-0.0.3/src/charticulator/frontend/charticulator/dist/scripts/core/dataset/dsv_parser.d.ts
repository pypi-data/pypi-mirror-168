import { LocaleNumberFormat } from "./data_types";
import { Table } from "./dataset";
export declare function parseHints(hints: string): {
    [name: string]: string;
};
export interface LocaleFileFormat {
    delimiter: string;
    numberFormat: LocaleNumberFormat;
    currency: string;
    group: string;
    utcTimeZone: boolean;
}
/**
 * Parses data from file. Returns converted rows and list of colum names with types.
 * Calls {@link inferAndConvertColumn} method from {@link "core/dataset/data_types"} for convert types.
 * @param fileName input file name for parsing
 * @param content data of file
 * @param type type of file. *.csv - text with coma delimeter. *.tsv - tab separated text files
 */
export declare function parseDataset(fileName: string, content: string, localeFileFormat: LocaleFileFormat): Table;
