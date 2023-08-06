import * as React from "react";
import { AppStore } from "../../stores";
export interface FileViewOptionsProps {
    onClose: () => void;
}
export declare const FileViewOptionsView: React.FC<FileViewOptionsProps>;
export declare class FileViewOptions extends React.Component<{
    onClose: () => void;
    store: AppStore;
}, Record<string, unknown>> {
    render(): JSX.Element;
}
