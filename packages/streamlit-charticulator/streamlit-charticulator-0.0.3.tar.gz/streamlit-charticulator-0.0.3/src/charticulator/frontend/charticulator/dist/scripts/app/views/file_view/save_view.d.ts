import * as React from "react";
import { AppStore } from "../../stores";
export interface FileViewSaveAsProps {
    onClose: () => void;
    store: AppStore;
}
export interface FileViewSaveAsState {
    saving?: boolean;
    error?: string;
}
export declare class FileViewSaveAs extends React.Component<FileViewSaveAsProps, FileViewSaveAsState> {
    state: FileViewSaveAsState;
    render(): JSX.Element;
}
