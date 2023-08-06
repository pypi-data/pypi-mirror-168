import { ConstraintPlugin } from "../abstract";
import { PolarAttributes, PolarProperties } from "../../prototypes/plot_segments/region_2d/polar";
import { Constraint } from "../../specification";
import { ChartStateManager } from "../../prototypes";
export declare class PolarPlotSegmentPlugin extends ConstraintPlugin {
    private attrs;
    private chartConstraints;
    private objectID;
    private manager;
    private properties;
    constructor(attrs: PolarAttributes, chartConstraints: Constraint[], objectID: string, manager: ChartStateManager, properties: PolarProperties);
    apply(): boolean;
}
