import { Style } from "../../graphics";
import { MarkClass } from "./mark";
import { ObjectClass } from "../object";
import { ObjectState, EmphasisMethod, AttributeMap } from "../../specification";
import { Specification } from "../../../container";
export declare const DEFAULT_EMPHASIS_STROKE_COLOR: {
    r: number;
    g: number;
    b: number;
};
export declare const DEFAULT_EMPHASIS_STROKE_WIDTH = 1;
export declare const DEFAULT_POWER_BI_OPACITY = 0.4;
/**
 * Represents a mark class that is emphasizable
 */
export declare abstract class EmphasizableMarkClass<PropertiesType extends AttributeMap = AttributeMap, AttributesType extends AttributeMap = AttributeMap> extends MarkClass<PropertiesType, AttributesType> {
    private defaultMethod;
    constructor(parent: ObjectClass, object: Specification.Object<PropertiesType>, state: ObjectState<AttributesType>, defaultMethod?: EmphasisMethod);
    /**
     * Generates styling info for styling emphasized marks
     * @param emphasize If true, emphasis will be applied.
     */
    protected generateEmphasisStyle(emphasize?: boolean): Style;
}
