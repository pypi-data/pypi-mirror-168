import { MainView } from "./main_view";
import { AppStore } from "./stores";
import { Dispatcher, Specification, Dataset, Prototypes } from "../core";
import { ExtensionContext, Extension } from "./extension";
import { Action } from "./actions/actions";
import { CharticulatorWorkerInterface } from "../worker";
import { CharticulatorAppConfig } from "./config";
import { ExportTemplateTarget } from "./template";
import { MenuBarHandlers, MenubarTabButton } from "./views/menubar";
import { TelemetryRecorder } from "./components";
import { AttributeMap } from "../core/specification";
import { EditorType } from "./stores/app_store";
import { LocalizationConfig } from "../container/container";
export declare class ApplicationExtensionContext implements ExtensionContext {
    app: Application;
    constructor(app: Application);
    getGlobalDispatcher(): Dispatcher<Action>;
    /** Get the store */
    getAppStore(): AppStore;
    getApplication(): Application;
}
export declare const enum NestedEditorMessageType {
    Save = "save",
    Initialized = "initialized"
}
export interface NestedEditorMessage {
    id: string;
    type: NestedEditorMessageType;
    specification?: Specification.Chart;
    template?: Specification.Template.ChartTemplate;
}
export declare enum NestedEditorEventType {
    Load = "load",
    Save = "save"
}
export interface NestedEditorData {
    id: string;
    type: NestedEditorEventType;
    dataset: Dataset.Dataset;
    specification: Specification.Chart;
    originSpecification?: Specification.Chart;
    template: Specification.Template.ChartTemplate;
    width: number;
    height: number;
    filterCondition: {
        column: string;
        value: any;
    };
}
export declare class Application {
    worker: CharticulatorWorkerInterface;
    appStore: AppStore;
    mainView: MainView;
    extensionContext: ApplicationExtensionContext;
    private config;
    private containerID;
    private nestedEditor;
    destroy(): void;
    initialize(config: CharticulatorAppConfig, containerID: string, workerConfig: {
        workerScriptContent?: string;
        worker?: CharticulatorWorkerInterface;
    }, localizaiton: LocalizationConfig, utcTimeZone: boolean, handlers?: {
        menuBarHandlers?: MenuBarHandlers;
        telemetry?: TelemetryRecorder;
        tabButtons?: MenubarTabButton[];
        nestedEditor?: {
            onOpenEditor: (options: Prototypes.Controls.NestedChartEditorOptions, object: Specification.Object<AttributeMap>, property: Prototypes.Controls.Property) => void;
        };
    }): Promise<void>;
    setupNestedEditor(id: string, onInitialized?: (id: string, load: (data: NestedEditorData) => void) => void, onSave?: (data: any) => void, onClose?: () => void, editorMode?: EditorType): void;
    processHashString(): Promise<void>;
    addExtension(extension: Extension): void;
    registerExportTemplateTarget(name: string, ctor: (template: Specification.Template.ChartTemplate) => ExportTemplateTarget): void;
    unregisterExportTemplateTarget(name: string): void;
}
