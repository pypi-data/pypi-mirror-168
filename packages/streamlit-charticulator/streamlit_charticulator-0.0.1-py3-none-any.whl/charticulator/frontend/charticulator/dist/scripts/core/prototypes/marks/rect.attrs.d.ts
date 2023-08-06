import { AttributeDescriptions } from "../object";
import { Color } from "../../common";
import { AttributeMap } from "../../specification/index";
import { StrokeStyle } from "../common";
import { ShapeType } from "./rect";
import { OrientationType } from "../../prototypes/legends/types";
export declare const rectAttributes: AttributeDescriptions;
/**
 * Properties of rectangle
 *   -------------- y1
 *   |            |     |
 *   |            | yc  height
 *   |            |     |
 *   -------------- y2
 *  x1     xc     x2
 *  <----width---->
 */
export interface RectElementAttributes extends AttributeMap {
    /** x value of left top point of rect */
    x1: number;
    /** y value of left top point of rect */
    y1: number;
    /** x value of right bottom point of rect */
    x2: number;
    /** y value of right bottom point of rect */
    y2: number;
    /** x value of center point of rect */
    cx: number;
    /** y value of center point of rect */
    cy: number;
    /** width of rectangle */
    width: number;
    /** height of rectangle */
    height: number;
    /** color of the rectangle border  */
    stroke: Color;
    /** color of the rectangle  */
    fill: Color;
    /** thickness of the rectangle border */
    strokeWidth: number;
    /** opacity */
    opacity: number;
    /** visual state of rectangle */
    visible: boolean;
    rx: number;
    ry: number;
}
export interface RectElementProperties extends AttributeMap {
    shape: ShapeType;
    strokeStyle: StrokeStyle;
    allowFlipping: boolean;
    rx: number;
    ry: number;
    orientation: OrientationType;
    cometMark: boolean;
}
