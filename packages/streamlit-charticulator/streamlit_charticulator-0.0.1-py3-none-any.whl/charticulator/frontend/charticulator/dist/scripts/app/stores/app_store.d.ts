import { Dataset, Expression, MessageType, Prototypes, Solver, Specification } from "../../core";
import { BaseStore } from "../../core/store/base";
import { CharticulatorWorkerInterface } from "../../worker";
import { Actions, DragData } from "../actions";
import { AbstractBackend } from "../backend/abstract";
import { ExportTemplateTarget } from "../template";
import { ActionHandlerRegistry } from "./action_handlers";
import { HistoryManager } from "./history_manager";
import { Selection } from "./selection";
import { LocaleFileFormat } from "../../core/dataset/dsv_parser";
import { TableType } from "../../core/dataset";
import { ValueType } from "../../core/expression/classes";
import { DataKind, DataType } from "../../core/specification";
import { RenderEvents } from "../../core/graphics";
import { AxisDataBinding, AxisDataBindingType, CollapseOrExpandPanels, NumericalMode } from "../../core/specification/types";
import { ObjectClass } from "../../core/prototypes";
export interface ChartStoreStateSolverStatus {
    solving: boolean;
}
export interface SelectionState {
    selection?: {
        type: string;
        chartElementID?: string;
        glyphID?: string;
        markID?: string;
        glyphIndex?: number;
    };
    currentGlyphID?: string;
}
export interface AppStoreState {
    version: string;
    originDataset?: Dataset.Dataset;
    dataset: Dataset.Dataset;
    chart: Specification.Chart;
    chartState: Specification.ChartState;
}
export interface ScaleInferenceOptions {
    expression: string;
    valueType: Specification.DataType;
    valueKind: Specification.DataKind;
    outputType: Specification.AttributeType;
    hints?: Prototypes.DataMappingHints;
    markAttribute?: string;
}
export declare enum EditorType {
    Nested = "nested",
    Embedded = "embedded",
    NestedEmbedded = "nestedembedded",
    Chart = "chart"
}
export declare class AppStore extends BaseStore {
    static EVENT_IS_NESTED_EDITOR: string;
    static EVENT_NESTED_EDITOR_EDIT: string;
    static EVENT_NESTED_EDITOR_CLOSE: string;
    /** Fires when the dataset changes */
    static EVENT_DATASET: string;
    /** Fires when the chart state changes */
    static EVENT_GRAPHICS: string;
    /** Fires when the selection changes */
    static EVENT_SELECTION: string;
    /** Fires when the current tool changes */
    static EVENT_CURRENT_TOOL: string;
    /** Fires when solver status changes */
    static EVENT_SOLVER_STATUS: string;
    /** Fires when the chart was saved */
    static EVENT_SAVECHART: string;
    /** Fires when user clicks Edit nested chart for embedded editor */
    static EVENT_OPEN_NESTED_EDITOR: string;
    /** The WebWorker for solving constraints */
    readonly worker: CharticulatorWorkerInterface;
    /** Is this app a nested chart editor? */
    editorType: EditorType;
    /** Should we disable the FileView */
    disableFileView: boolean;
    /** The dataset created on import */
    originDataset: Dataset.Dataset;
    /** The current dataset */
    dataset: Dataset.Dataset;
    /** The current chart */
    chart: Specification.Chart;
    /** The current chart state */
    chartState: Specification.ChartState;
    version: string;
    /** Rendering Events */
    renderEvents?: RenderEvents;
    currentSelection: Selection;
    currentAttributeFocus: string;
    currentMappingAttributeFocus: string;
    currentGlyph: Specification.Glyph;
    protected selectedGlyphIndex: {
        [id: string]: number;
    };
    protected localeFileFormat: LocaleFileFormat;
    currentTool: string;
    currentToolOptions: string;
    searchString: string;
    collapseOrExpandPanelsType: CollapseOrExpandPanels;
    chartManager: Prototypes.ChartStateManager;
    solverStatus: ChartStoreStateSolverStatus;
    /** Manages the history of states */
    historyManager: HistoryManager<AppStoreState>;
    /** The backend that manages data */
    backend: AbstractBackend;
    /** The id of the currently editing chart */
    currentChartID: string;
    actionHandlers: ActionHandlerRegistry<AppStore, Actions.Action>;
    private propertyExportName;
    messageState: Map<MessageType | string, string>;
    constructor(worker: CharticulatorWorkerInterface, dataset: Dataset.Dataset);
    setPropertyExportName(propertyName: string, value: string): void;
    getPropertyExportName(propertyName: string): string;
    saveState(): AppStoreState;
    saveDecoupledState(): AppStoreState;
    loadState(state: AppStoreState): void;
    saveHistory(): void;
    renderSVG(): string;
    renderLocalSVG(): Promise<string>;
    handleAction(action: Actions.Action): void;
    backendOpenChart(id: string): Promise<void>;
    private updateChartState;
    backendSaveChart(): Promise<void>;
    backendSaveChartAs(name: string): Promise<string>;
    setupNestedEditor(callback: (newSpecification: Specification.Chart) => void, type: EditorType): void;
    private registeredExportTemplateTargets;
    registerExportTemplateTarget(name: string, ctor: (template: Specification.Template.ChartTemplate) => ExportTemplateTarget): void;
    unregisterExportTemplateTarget(name: string): void;
    listExportTemplateTargets(): string[];
    createExportTemplateTarget(name: string, template: Specification.Template.ChartTemplate): ExportTemplateTarget;
    getTable(name: string): Dataset.Table;
    getTables(): Dataset.Table[];
    getColumnVector(table: Dataset.Table, columnName: string): Dataset.DataValue[];
    saveSelectionState(): SelectionState;
    loadSelectionState(selectionState: SelectionState): void;
    setSelectedGlyphIndex(plotSegmentID: string, glyphIndex: number): void;
    getSelectedGlyphIndex(plotSegmentID: string): number;
    getMarkIndex(mark: Specification.Glyph): number;
    forAllGlyph(glyph: Specification.Glyph, callback: (glyphState: Specification.GlyphState, plotSegment: Specification.PlotSegment, plotSegmentState: Specification.PlotSegmentState) => void): void;
    preSolveValues: [Solver.ConstraintStrength, Specification.AttributeMap, string, number][];
    addPresolveValue(strength: Solver.ConstraintStrength, state: Specification.AttributeMap, attr: string, value: number): void;
    /** Given the current selection, find a reasonable plot segment for a glyph */
    findPlotSegmentForGlyph(glyph: Specification.Glyph): Specification.PlotSegment<Specification.ObjectProperties>;
    scaleInference(context: {
        glyph?: Specification.Glyph;
        chart?: {
            table: string;
        };
    }, options: ScaleInferenceOptions): string;
    isLegendExistForScale(scale: string): boolean;
    toggleLegendForScale(scale: string, mapping: Specification.ScaleMapping, plotSegment: ObjectClass): void;
    getRepresentativeGlyphState(glyph: Specification.Glyph): Specification.GlyphState<Specification.AttributeMap>;
    solveConstraintsAndUpdateGraphics(mappingOnly?: boolean): void;
    solveConstraintsInWorker(mappingOnly?: boolean): Promise<void>;
    newChartEmpty(): void;
    deleteSelection(): void;
    handleEscapeKey(): void;
    getClosestSnappingGuide(point: {
        x: number;
        y: number;
    }): {
        element: any;
        guide: Prototypes.SnappingGuides.Description;
    }[];
    buildChartTemplate(): Specification.Template.ChartTemplate;
    verifyUserExpressionWithTable(inputString: string, table: string, options?: Expression.VerifyUserExpressionOptions): Expression.VerifyUserExpressionReport;
    updateScales(): void;
    getDataKindByType: (type: AxisDataBindingType) => DataKind;
    updatePlotSegments(): void;
    updateDataAxes(): void;
    private getBindingByDataKind;
    bindDataToAxis(options: {
        object: Specification.PlotSegment;
        property?: string;
        appendToProperty?: string;
        dataExpression: DragData.DataExpression;
        type?: AxisDataBindingType;
        numericalMode?: NumericalMode;
        autoDomainMax: boolean;
        autoDomainMin: boolean;
        domainMin: number;
        domainMax: number;
        defineCategories: boolean;
    }): void;
    /**
     * Due to undefined "value" will not saved after JSON.stringfy, need to update all undefined "values" to null
     * deepClone uses JSON.stringfy to create copy of object. If object losses some property after copy
     * the function expect_deep_approximately_equals gives difference for identical tempalte/chart state
     * See {@link ChartStateManager.hasUnsavedChanges} for details
     * @param dataExpression Data expression for axis
     */
    private normalizeDataExpression;
    getCategoriesForOrderByColumn(orderExpression: string, expression: string, data: AxisDataBinding): string[];
    getCategoriesForDataBinding(metadata: Dataset.ColumnMetadata, type: DataType, values: ValueType[]): {
        categories: string[];
        order: string[];
    };
    getGroupingExpression(object: Specification.Object<Specification.ObjectProperties>): Specification.Types.GroupBy;
    getLocaleFileFormat(): LocaleFileFormat;
    setLocaleFileFormat(value: LocaleFileFormat): void;
    checkColumnsMapping(column: Specification.Template.Column, tableType: TableType, dataset: Dataset.Dataset): Specification.Template.Column[];
    setProperty(config: {
        object: Specification.Object;
        property: string;
        field: number | string | (number | string)[];
        value: Specification.AttributeValue;
        noUpdateState?: boolean;
        noComputeLayout?: boolean;
    }): void;
}
