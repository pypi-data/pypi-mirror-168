import { Specification } from "../..";
import { ChartStateManager } from "../../prototypes";
import { PolarGuideCoordinatorAttributesExtend } from "../../prototypes/guides/polar_coordinator";
import { ConstraintPlugin, ConstraintSolver, Variable } from "../abstract";
export interface PolarCoordinatorPluginOptions {
}
export declare class PolarCoordinatorPlugin extends ConstraintPlugin {
    solver: ConstraintSolver;
    cx: Variable;
    cy: Variable;
    an: Variable[];
    attrs: PolarGuideCoordinatorAttributesExtend;
    radialVarable: Variable[];
    angleVarable: Variable[];
    chartConstraints: Specification.Constraint[];
    coordinatoObjectID: string;
    chartMananger: ChartStateManager;
    constructor(solver: ConstraintSolver, cx: Variable, cy: Variable, radialVarable: Variable[], angleVarable: Variable[], attrs: PolarGuideCoordinatorAttributesExtend, chartConstraints: Specification.Constraint[], coordinatoObjectID: string, chartMananger: ChartStateManager);
    apply(): boolean;
}
