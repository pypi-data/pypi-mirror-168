import { Rect } from "../../../container";
import { AxisMode } from "../../prototypes/plot_segments/axis";
import { ConstraintPlugin, ConstraintSolver, Variable } from "../abstract";
export interface PackingPluginOptions {
    gravityX: number;
    gravityY: number;
    boxed?: Rect;
}
export declare class PackingPlugin extends ConstraintPlugin {
    solver: ConstraintSolver;
    cx: Variable;
    cy: Variable;
    points: [Variable, Variable, number][];
    xEnable: boolean;
    yEnable: boolean;
    getXYScale: () => {
        x: number;
        y: number;
    };
    gravityX?: number;
    gravityY?: number;
    boxed?: Rect;
    constructor(solver: ConstraintSolver, cx: Variable, cy: Variable, points: [Variable, Variable, number][], axisOnly?: AxisMode, getXYScale?: () => {
        x: number;
        y: number;
    }, options?: PackingPluginOptions);
    apply(): boolean;
}
