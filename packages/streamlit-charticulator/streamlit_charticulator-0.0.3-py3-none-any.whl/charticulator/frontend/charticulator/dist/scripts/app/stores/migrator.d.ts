import { AppStoreState } from "./app_store";
import { Specification } from "../../core";
/** Upgrade old versions of chart spec and state to newer version */
export declare class Migrator {
    migrate(state: AppStoreState, targetVersion: string): AppStoreState;
    /**
     * Adds enableTooltips, enableSelection, enableContextMenu properties with default balue true
     * @param state current state
     */
    addInteractivityProperties(state: AppStoreState): AppStoreState;
    addOriginDataSet(state: AppStoreState): AppStoreState;
    addScaleMappings(state: AppStoreState): AppStoreState;
    addTableTypes(state: AppStoreState): AppStoreState;
    fixDataRowIndices(state: AppStoreState): AppStoreState;
    addAggregationToExpression(expr: string, valueType: string): string;
    fixAxisDataMapping(mapping: Specification.Types.AxisDataBinding): void;
    fixDataMappingExpressions(state: AppStoreState): AppStoreState;
    fixLinkOrder_v130(state: AppStoreState): AppStoreState;
    setValueToLayoutPropertyOfLegend(state: AppStoreState): AppStoreState;
    setValueItemShapeOfLegend(state: AppStoreState): AppStoreState;
    setPolarAngularLegend(state: AppStoreState): AppStoreState;
    private updateAxis;
    setMissedProperties(state: AppStoreState): AppStoreState;
    setAllowFlipToMarks(state: AppStoreState): AppStoreState;
    setMissedGlyphRectProperties(state: AppStoreState): AppStoreState;
    private parseExpression;
    setMissedSortProperties(state: AppStoreState): AppStoreState;
    setMissedLegendProperties(state: AppStoreState): AppStoreState;
    setMissedProperties_2_1_6(state: AppStoreState): AppStoreState;
}
