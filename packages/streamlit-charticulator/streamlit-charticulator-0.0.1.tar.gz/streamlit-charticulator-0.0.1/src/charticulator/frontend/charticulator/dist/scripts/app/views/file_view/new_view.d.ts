import * as React from "react";
import { AppStore } from "../../stores";
interface FileViewNewProps {
    store: AppStore;
    onClose: () => void;
}
export declare class FileViewNew extends React.Component<FileViewNewProps, Record<string, unknown>> {
    render(): JSX.Element;
}
export {};
