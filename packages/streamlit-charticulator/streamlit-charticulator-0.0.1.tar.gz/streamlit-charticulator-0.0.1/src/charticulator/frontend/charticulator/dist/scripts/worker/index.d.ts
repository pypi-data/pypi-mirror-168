import { CharticulatorCoreConfig, Dataset, Solver, Specification } from "../core";
import { WorkerRPC } from "./communication";
export { CharticulatorWorkerProcess } from "./worker_main";
export interface CharticulatorWorkerInterface {
    initialize(config: CharticulatorCoreConfig): Promise<any>;
    solveChartConstraints: (chart: Specification.Chart, chartState: Specification.ChartState, dataset: Dataset.Dataset, preSolveValues: [Solver.ConstraintStrength, Specification.AttributeMap, string, number][], mappingOnly: boolean) => Promise<any> | any;
}
/**
 * The representation of the background worker. This is used from the main process.
 */
export declare class CharticulatorWorker extends WorkerRPC implements CharticulatorWorkerInterface {
    constructor(workerLocation: string);
    initialize(config: CharticulatorCoreConfig): Promise<void>;
    solveChartConstraints(chart: Specification.Chart, chartState: Specification.ChartState, dataset: Dataset.Dataset, preSolveValues: [Solver.ConstraintStrength, Specification.AttributeMap, string, number][], mappingOnly?: boolean): Promise<Specification.ChartState<Specification.AttributeMap>>;
}
