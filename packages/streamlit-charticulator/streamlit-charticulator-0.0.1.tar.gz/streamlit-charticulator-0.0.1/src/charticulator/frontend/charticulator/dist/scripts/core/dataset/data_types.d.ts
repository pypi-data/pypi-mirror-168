import { DataValue, DataType, ColumnMetadata } from "./dataset";
import { LocaleFileFormat } from "./dsv_parser";
export interface LocaleNumberFormat {
    remove: string;
    decimal: string;
}
export interface DataTypeDescription {
    test: (v: string, localeNumberFormat?: LocaleNumberFormat) => boolean;
    convert: (v: string, localeNumberFormat?: LocaleNumberFormat | number) => DataValue;
}
export declare const dataTypes: {
    [name in DataType]: DataTypeDescription;
};
/** Infer column type from a set of strings (not null) */
export declare function inferColumnType(values: string[], localeNumberFormat: LocaleNumberFormat): DataType;
/** Convert strings to value type, null & non-convertibles are set as null */
export declare function convertColumn(type: DataType, values: string[], localeNumberFormat?: LocaleNumberFormat, timeZone?: number): DataValue[];
/** Get distinct values from a non-null array of basic types */
export declare function getDistinctValues(values: DataValue[]): DataValue[];
/** Infer column metadata and update type if necessary */
export declare function inferAndConvertColumn(values: string[], localeFileFormat: LocaleFileFormat, hints?: {
    [name: string]: string;
}): {
    values: DataValue[];
    rawValues?: string[] | DataValue[];
    type: DataType;
    metadata: ColumnMetadata;
};
export declare function convertColumnType(values: any[], type: DataType): DataValue[];
export declare function isBase64Image(string: string): boolean;
