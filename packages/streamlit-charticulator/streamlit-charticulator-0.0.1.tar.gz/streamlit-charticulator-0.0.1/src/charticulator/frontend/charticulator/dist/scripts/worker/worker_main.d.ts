import { CharticulatorWorkerInterface } from ".";
import * as Core from "../core";
import { WorkerHostProcess } from "./communication";
export declare class CharticulatorWorkerProcess extends WorkerHostProcess implements CharticulatorWorkerInterface {
    constructor();
    initialize(config: Core.CharticulatorCoreConfig): Promise<void>;
    solveChartConstraints(chart: Core.Specification.Chart, chartState: Core.Specification.ChartState, dataset: Core.Dataset.Dataset, preSolveValues?: [Core.Solver.ConstraintStrength, Core.Specification.AttributeMap, string, number][], mappingOnly?: boolean): Core.Specification.ChartState<Core.Specification.AttributeMap>;
    doSolveChartConstraints(chart: Core.Specification.Chart, chartState: Core.Specification.ChartState, dataset: Core.Dataset.Dataset, additional?: (solver: Core.Solver.ChartConstraintSolver) => void, mappingOnly?: boolean): Core.Specification.ChartState<Core.Specification.AttributeMap>;
}
