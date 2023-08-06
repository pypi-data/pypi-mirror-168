import * as React from "react";
export declare enum TelemetryActionType {
    Exception = "exception",
    ExportTemplate = "exportTempalte"
}
export interface TelemetryRecorder {
    record(type: TelemetryActionType, payload: Record<string, any>): void;
}
export interface ErrorBoundaryProps {
    maxWidth?: number;
    telemetryRecorder?: TelemetryRecorder;
}
export declare const TelemetryContext: React.Context<TelemetryRecorder>;
export declare class ErrorBoundary extends React.Component<ErrorBoundaryProps, {
    hasError: boolean;
    errorString?: string;
}> {
    constructor(props: ErrorBoundaryProps);
    componentDidCatch(error: Error, info: React.ErrorInfo): void;
    render(): any;
}
