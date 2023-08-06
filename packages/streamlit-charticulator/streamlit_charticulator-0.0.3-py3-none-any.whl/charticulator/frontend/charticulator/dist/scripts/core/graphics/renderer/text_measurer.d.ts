import { Graphics } from "../..";
export interface TextMeasurement {
    width: number;
    fontSize: number;
    ideographicBaseline: number;
    hangingBaseline: number;
    alphabeticBaseline: number;
    middle: number;
}
export declare class TextMeasurer {
    canvas: HTMLCanvasElement;
    context: CanvasRenderingContext2D;
    fontFamily: string;
    fontSize: number;
    static parameters: {
        hangingBaseline: number[];
        ideographicBaseline: number[];
        alphabeticBaseline: number[];
        middle: number[];
    };
    constructor();
    setFontFamily(family: string): void;
    setFontSize(size: number): void;
    measure(text: string): TextMeasurement;
    private static globalInstance;
    static GetGlobalInstance(): Graphics.TextMeasurer;
    static Measure(text: string, family: string, size: number): Graphics.TextMeasurement;
    static ComputeTextPosition(x: number, y: number, metrics: TextMeasurement, alignX?: "left" | "middle" | "right", alignY?: "top" | "middle" | "bottom", xMargin?: number, yMargin?: number): [number, number];
}
export declare const SPACE = " ";
export declare const BREAKERS_REGEX: RegExp;
export declare function split(str: string): string[];
/**
 * Splits text to fragments do display text with word wrap
 * Source code taken from https://github.com/microsoft/powerbi-visuals-utils-formattingutils/blob/master/src/wordBreaker.ts#L130
 * @param content source of text
 * @param maxWidth max available with for text
 * @param maxNumLines limit lines count, rest of words will be drew in the last line
 * @param fontFamily font family
 * @param fontSize font size in px
 */
export declare function splitByWidth(content: string, maxWidth: number, maxNumLines: number, fontFamily: string, fontSize: number): string[];
