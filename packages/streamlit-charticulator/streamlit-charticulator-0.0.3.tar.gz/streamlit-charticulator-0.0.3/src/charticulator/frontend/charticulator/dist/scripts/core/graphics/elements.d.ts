/**
 * Internal graphics representation
 * Bridge the core components with the rendering system
 *
 * Coordinate System:
 *        y
 *        ^
 *        |
 *   -----o-----> x
 *        |
 *        |
 *
 * Rigid Transform:
 *
 *  (theta is counter clockwise in above diagram)
 *  x' = x cos(theta) - y sin(theta) + tx
 *  y' = x sin(theta) + y cos(theta) + ty
 *
 *  concatTransform(a, b)(p) = a(b(p))
 *
 * @packageDocumentation
 * @preferred
 */
import * as React from "react";
import { Color, Point } from "../common";
import * as Specification from "../specification";
import * as Dataset from "../dataset";
import { ArrowType } from "../../core/prototypes/links";
export interface PointDirection extends Point {
    direction: Point;
}
export interface RigidTransform {
    x: number;
    y: number;
    angle: number;
}
/** Specify a modification to a numeric value: (v' = set) or (v' = (v * multiply + add) ^ pow) */
export interface NumberModifier {
    /** Set to a specific value */
    set?: number;
    /** Multiply a scaler to */
    multiply?: number;
    /** Add the amount to */
    add?: number;
    /** Apply a pow function to */
    pow?: number;
}
export interface ColorFilter {
    saturation?: NumberModifier;
    lightness?: NumberModifier;
}
export interface Style {
    strokeColor?: Color;
    strokeOpacity?: number;
    strokeWidth?: number;
    strokeDasharray?: string;
    strokeLinejoin?: "round" | "miter" | "bevel";
    strokeLinecap?: "round" | "butt" | "square";
    colorFilter?: ColorFilter;
    fillColor?: Color;
    backgroundColor?: Color;
    backgroundColorId?: string;
    fillOpacity?: number;
    /** The opacity of this element */
    opacity?: number;
    /** Text anchor position */
    textAnchor?: "start" | "middle" | "end";
    startArrowColorId?: string;
    endArrowColorId?: string;
}
export interface Interactable {
    onClick?: (event: React.MouseEvent<globalThis.Element>) => void;
    onMousedown?: (event: React.MouseEvent<globalThis.Element>) => void;
    onMouseup?: (event: React.MouseEvent<globalThis.Element>) => void;
    onMousewheel?: (event: React.MouseEvent<globalThis.Element>) => void;
    onMousemove?: (event: React.MouseEvent<globalThis.Element>) => void;
}
export interface Selectable {
    plotSegment: Specification.PlotSegment;
    glyphIndex: number;
    rowIndices: number[];
    enableTooltips?: boolean;
    enableSelection?: boolean;
    enableContextMenu?: boolean;
}
export interface Element {
    type: string;
    style?: Style;
    selectable?: Selectable;
    interactable?: Interactable;
}
export interface ChartContainerElement {
    type: "chart-container";
    chart: Specification.Chart;
    selectable: Selectable;
    dataset: Dataset.Dataset;
    x: number;
    y: number;
    width: number;
    height: number;
}
export interface Rect extends Element {
    type: "rect";
    x1: number;
    y1: number;
    x2: number;
    y2: number;
    rx?: number;
    ry?: number;
    rotation?: number;
}
export interface Line extends Element {
    type: "line";
    x1: number;
    y1: number;
    x2: number;
    y2: number;
}
export interface Polygon extends Element {
    type: "polygon";
    points: Point[];
}
export interface Path extends Element {
    type: "path";
    cmds: {
        cmd: string;
        args: number[];
    }[];
    transform: string;
    beginArrowType?: ArrowType;
    endArrowType?: ArrowType;
}
export interface Circle extends Element {
    type: "circle";
    cx: number;
    cy: number;
    r: number;
}
export interface Ellipse extends Element {
    type: "ellipse";
    x1: number;
    y1: number;
    x2: number;
    y2: number;
}
export interface Text extends Element {
    type: "text";
    cx: number;
    cy: number;
    text: string;
    fontFamily: string;
    fontSize: number;
}
export declare enum PathTextAlignment {
    Start = "start",
    Middle = "middle",
    End = "end"
}
export interface TextOnPath extends Element {
    type: "text-on-path";
    pathCmds: Path["cmds"];
    align: PathTextAlignment;
    text: string;
    fontFamily: string;
    fontSize: number;
}
export interface Image extends Element {
    type: "image";
    src: string;
    x: number;
    y: number;
    width: number;
    height: number;
    /** Size mode, default to letterbox */
    mode?: "letterbox" | "stretch";
}
export interface Group extends Element {
    type: "group";
    key?: string;
    transform: RigidTransform;
    elements: Element[];
}
export declare function makeRect(x1: number, y1: number, x2: number, y2: number, style?: Style, rx?: number, ry?: number): Rect;
export declare function makeCircle(cx: number, cy: number, r: number, style?: Style): Circle;
export declare function makeEllipse(x1: number, y1: number, x2: number, y2: number, style?: Style): Ellipse;
export declare function makeGroup(elements: Element[]): Group;
export declare function makeLine(x1: number, y1: number, x2: number, y2: number, style?: Style): Line;
export declare function makePolygon(points: Point[], style?: Style): Polygon;
export declare function makeText(cx: number, cy: number, text: string, fontFamily: string, fontSize: number, style?: Style, selectable?: Selectable): Text;
export declare class PathMaker {
    path: Path;
    currentX: number;
    currentY: number;
    moveTo(x: number, y: number): void;
    lineTo(x: number, y: number): void;
    transformRotation(angle: number, x?: number, y?: number): void;
    setBeginArrowType(arrowType: ArrowType): void;
    setEndArrowType(arrowType: ArrowType): void;
    cubicBezierCurveTo(c1x: number, c1y: number, c2x: number, c2y: number, x: number, y: number): void;
    quadraticBezierCurveTo(cx: number, cy: number, x: number, y: number): void;
    arcTo(rx: number, ry: number, xAxisRotation: number, largeArcFlag: number, sweepFlag: number, x: number, y: number): void;
    /** Compose a Archimedean spiral with r = a + b theta, theta from thetaMin to thetaMax */
    archimedeanSpiral(cx: number, cy: number, a: number, b: number, thetaMin: number, thetaMax: number, moveTo?: boolean): void;
    polarLineTo(cx: number, cy: number, angle1: number, r1: number, angle2: number, r2: number, moveTo?: boolean): void;
    closePath(): void;
}
export declare function makePath(style?: Style): PathMaker;
export declare function translation(x?: number, y?: number): RigidTransform;
export declare function rotation(angle: number): RigidTransform;
/** Concat two transforms, f(p) := a(b(p))  */
export declare function concatTransform(a: RigidTransform, b: RigidTransform): {
    x: number;
    y: number;
    angle: number;
};
export declare function transform(transform: RigidTransform, a: Point): Point;
export declare function transformDirection(transform: RigidTransform, a: Point): Point;
