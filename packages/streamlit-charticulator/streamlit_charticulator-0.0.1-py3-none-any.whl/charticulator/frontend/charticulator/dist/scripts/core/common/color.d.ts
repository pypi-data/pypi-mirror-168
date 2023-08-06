import { Colorspace } from "../../app/components/fluent_ui_gradient_picker";
/** Color in RGB */
export interface Color {
    r: number;
    g: number;
    b: number;
}
/** Color gradient */
export interface ColorGradient {
    colorspace: Colorspace;
    colors: Color[];
}
/** Get Color from HTML color string */
export declare function colorFromHTMLColor(html: string): Color;
export declare function parseColorOrThrowException(html: string): Color;
export declare function colorToHTMLColor(color: Color): string;
export declare function colorToHTMLColorHEX(color: Color): string;
export declare type ColorConverter = (a: number, b: number, c: number) => [number, number, number] | [number, number, number, boolean];
export declare function getColorConverter(from: string, to: string): ColorConverter;
export declare type ColorInterpolation = (t: number) => Color;
export declare function interpolateColor(from: Color, to: Color, colorspace?: string): ColorInterpolation;
export declare function interpolateColors(colors: Color[], colorspace?: string): ColorInterpolation;
export declare function setDefaultColorPaletteGenerator(generatorFunction: (key: string) => Color): void;
export declare function getDefaultColorPaletteGenerator(): (key: string) => Color;
export declare function setDefaultColorGeneratorResetFunction(resetFunction: () => void): void;
export declare function getDefaultColorGeneratorResetFunction(): () => void;
export declare function getDefaultColorPaletteByValue(value: string): Color;
export declare function getDefaultColorPalette(count: number): Color[];
