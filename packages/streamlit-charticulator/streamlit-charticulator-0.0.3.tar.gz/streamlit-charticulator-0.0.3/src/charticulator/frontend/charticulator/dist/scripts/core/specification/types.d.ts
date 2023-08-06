import { Color } from "../common";
import { DataKind } from "../dataset";
import { StrokeStyle } from "../prototypes";
import { AttributeMap, Expression, DataType } from "./index";
export declare enum OrderMode {
    alphabetically = "alphabetically",
    occurrence = "occurrence",
    order = "order"
}
export declare type AxisSide = "default" | "opposite";
export declare enum AxisDataBindingType {
    Default = "default",
    Numerical = "numerical",
    Categorical = "categorical"
}
export declare enum NumericalMode {
    Linear = "linear",
    Logarithmic = "logarithmic",
    Temporal = "temporal"
}
export declare enum TickFormatType {
    None = "none",
    Date = "date",
    Number = "number"
}
/** Common parameter and mapping types */
export interface AxisDataBinding extends AttributeMap {
    type: AxisDataBindingType;
    visible: boolean;
    side: AxisSide;
    /** Data mapping expression */
    expression?: Expression;
    rawExpression?: Expression;
    valueType?: DataType;
    /** Domain for linear/logarithm types */
    numericalMode?: NumericalMode;
    domainMin?: number;
    domainMax?: number;
    dataDomainMin?: number;
    dataDomainMax?: number;
    /** Export properties of axis for auto scale ranges */
    autoDomainMin?: boolean;
    autoDomainMax?: boolean;
    /** Categories for categorical type */
    categories?: string[];
    gapRatio?: number;
    /** Pre/post gap, will override the default with OR operation */
    enablePrePostGap?: boolean;
    tickDataExpression?: Expression;
    tickFormat?: string;
    tickFormatType?: TickFormatType;
    style?: AxisRenderingStyle;
    dataKind?: DataKind;
    order?: string[];
    orderMode?: OrderMode;
    /** scrolling options */
    allowScrolling?: boolean;
    allCategories?: string[];
    scrollPosition?: number;
    windowSize?: number;
    barOffset?: number;
    /** Offset options */
    offset?: number;
    /** render axis on top */
    onTop?: boolean;
    /** Order by another column */
    orderByExpression?: string;
    orderByCategories?: string[];
    enableSelection?: boolean;
    numberOfTicks?: number;
    autoNumberOfTicks?: boolean;
}
export interface AxisRenderingStyle extends AttributeMap {
    lineColor: Color;
    tickColor: Color;
    fontFamily: string;
    fontSize: number;
    tickSize: number;
    tickTextBackgroudColor: Color;
    tickTextBackgroudColorId: string;
    wordWrap: boolean;
    gridlineStyle: StrokeStyle;
    gridlineColor: Color;
    gridlineWidth: number;
    verticalText: boolean;
    showTicks: boolean;
    showBaseline: boolean;
}
export declare enum TextAlignmentHorizontal {
    Left = "left",
    Middle = "middle",
    Right = "right"
}
export declare enum TextAlignmentVertical {
    Top = "top",
    Middle = "middle",
    Bottom = "bottom"
}
export interface TextAlignment extends AttributeMap {
    x: TextAlignmentHorizontal;
    y: TextAlignmentVertical;
    xMargin: number;
    yMargin: number;
}
export declare enum Colorspace {
    Hcl = "hcl",
    Lab = "lab"
}
export interface ColorGradient extends AttributeMap {
    colorspace: Colorspace;
    colors: Color[];
}
export interface Image extends AttributeMap {
    src: string;
    width: number;
    height: number;
    name?: string;
}
/** LinkAnchor: specifies an anchor in a link */
export interface LinkAnchorPoint extends AttributeMap {
    /** X attribute reference */
    x: {
        element: string;
        attribute: string;
    };
    /** Y attribute reference */
    y: {
        element: string;
        attribute: string;
    };
    /** Link direction for curves */
    direction: {
        x: number;
        y: number;
    };
}
/** Filter specification, specify one of categories or expression */
export interface Filter extends AttributeMap {
    /** Filter by a categorical variable */
    categories?: {
        /** The expression to draw values from */
        expression: string;
        /** The accepted values */
        values: {
            [value: string]: boolean;
        };
    };
    /** Filter by an arbitrary expression */
    expression?: Expression;
}
/** GroupBy specification */
export interface GroupBy extends AttributeMap {
    /** Group by a string expression */
    expression?: Expression;
}
/** Order expression */
export interface SortBy extends AttributeMap {
    expression?: Expression;
}
export declare enum CollapseOrExpandPanels {
    Collapse = "collapse",
    Expand = "expand",
    Custom = "custom"
}
