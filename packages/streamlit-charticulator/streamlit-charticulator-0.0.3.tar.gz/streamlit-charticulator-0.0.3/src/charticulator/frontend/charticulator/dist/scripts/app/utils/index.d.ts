import { ZoomInfo, Dataset } from "../../core";
import { DataType, DataKind } from "../../core/specification";
export declare function classNames(...args: (string | [string, boolean])[]): string;
export declare function toSVGNumber(x: number): string;
export declare function toSVGZoom(zoom: ZoomInfo): string;
export declare function parseHashString(value: string): {
    [key: string]: string;
};
export interface RenderDataURLToPNGOptions {
    mode: "scale" | "thumbnail";
    scale?: number;
    thumbnail?: [number, number];
    background?: string;
}
export declare function renderDataURLToPNG(dataurl: string, options: RenderDataURLToPNGOptions): Promise<HTMLCanvasElement>;
export declare function readFileAsString(file: File): Promise<string>;
export declare function readFileAsDataUrl(file: File): Promise<string>;
export declare function getExtensionFromFileName(filename: string): string;
export declare function getFileNameWithoutExtension(filename: string): string;
export declare function showOpenFileDialog(accept?: string[]): Promise<File>;
export declare function b64EncodeUnicode(str: string): string;
export declare function stringToDataURL(mimeType: string, content: string): string;
export declare function getConvertableDataKind(type: DataType): DataKind[];
export declare function getPreferredDataKind(type: DataType): DataKind;
export declare function getConvertableTypes(type: DataType, dataSample?: (string | boolean | Date | number)[]): DataType[];
/** Fill table with values converted to @param type from origin table */
export declare function convertColumns(table: Dataset.Table, column: Dataset.Column, originTable: Dataset.Table, type: Dataset.DataType): string;
export declare function copyToClipboard(str: string): void;
export declare function isInIFrame(): boolean;
export declare function getAligntment(anchor: Element): {
    alignLeft: boolean;
    alignX: "end-inner" | "end-outer";
};
/** Test if a deep equals b with tolerance on numeric values */
export declare function expect_deep_approximately_equals(a: any, b: any, tol: number, weak?: boolean): void;
export declare function replaceUndefinedByNull(value: any): any;
