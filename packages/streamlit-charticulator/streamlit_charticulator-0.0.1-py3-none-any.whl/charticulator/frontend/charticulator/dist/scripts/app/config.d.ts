import { CharticulatorCoreConfig } from "../core";
export { MainViewConfig } from "./main_view";
import { MainViewConfig } from "./main_view";
export interface AppExtension {
    script: string | {
        src: string;
        sha256: string;
        integrity: string;
    };
    style: string;
    initialize: string;
}
export interface CharticulatorAppConfig extends CharticulatorCoreConfig {
    ContactUsHref?: string;
    LegalNotices: {
        /** HTML representation of the privacy statement */
        privacyStatementHTML: string;
    };
    /** Should we disable the file view */
    DisableFileView?: boolean;
    /** Load extensions */
    Extensions?: AppExtension[];
    /** Sample datasets to show */
    SampleDatasets?: {
        name: string;
        description: string;
        tables: {
            name: string;
            url: string;
            type: string;
        }[];
    }[];
    WorkerURL: string;
    ContainerURL: string;
    /** Deprecated. don't use */
    CorsPolicy: {
        TargetOrigins: string;
        Embedded: boolean;
    };
    MainView: MainViewConfig;
}
export declare function getConfig(): CharticulatorAppConfig;
