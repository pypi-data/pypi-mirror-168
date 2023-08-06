import { ValueType } from "./classes";
export declare const constants: {
    [name: string]: ValueType;
};
export declare const functions: {
    [name: string]: Function | {
        [name: string]: Function;
    } | any;
};
export declare const operators: {
    [name: string]: Function;
};
export declare const precedences: {
    LAMBDA_EXPRESSION: number;
    FUNCTION_ARGUMENT: number;
    OPERATORS: {
        [name: string]: number[];
    };
    FUNCTION_CALL: number;
    LAMBDA_FUNCTION: number;
    VARIABLE: number;
    FIELD_ACCESS: number;
    VALUE: number;
};
