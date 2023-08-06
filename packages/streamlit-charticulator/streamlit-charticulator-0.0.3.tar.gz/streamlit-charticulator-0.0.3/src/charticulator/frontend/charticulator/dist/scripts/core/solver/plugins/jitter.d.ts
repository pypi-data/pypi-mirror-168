import { AxisMode } from "../../prototypes/plot_segments/axis";
import { ConstraintPlugin, ConstraintSolver, Variable } from "../abstract";
export interface JitterPluginOptions {
    vertical: boolean;
    horizontal: boolean;
}
export declare class JitterPlugin extends ConstraintPlugin {
    solver: ConstraintSolver;
    x1: Variable;
    y1: Variable;
    x2: Variable;
    y2: Variable;
    points: [Variable, Variable, number][];
    xEnable: boolean;
    yEnable: boolean;
    getXYScale: () => {
        x: number;
        y: number;
    };
    options?: JitterPluginOptions;
    constructor(solver: ConstraintSolver, x1: Variable, y1: Variable, x2: Variable, y2: Variable, points: [Variable, Variable, number][], axisOnly?: AxisMode, options?: JitterPluginOptions);
    apply(): boolean;
}
