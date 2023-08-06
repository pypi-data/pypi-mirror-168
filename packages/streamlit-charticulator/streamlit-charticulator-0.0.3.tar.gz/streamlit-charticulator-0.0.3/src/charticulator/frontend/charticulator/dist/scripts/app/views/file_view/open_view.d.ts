import * as React from "react";
import { ItemDescription } from "../../backend/abstract";
import { AppStore } from "../../stores";
export interface FileViewOpenState {
    chartList: ItemDescription[];
    chartCount: number;
}
export declare class FileViewOpen extends React.Component<{
    onClose: () => void;
    store: AppStore;
}, FileViewOpenState> {
    state: FileViewOpenState;
    componentDidMount(): void;
    updateChartList(): void;
    renderChartList(): JSX.Element;
    render(): JSX.Element;
}
