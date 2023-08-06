import * as React from "react";
import { CharticulatorCoreConfig } from "../../core";
export interface TestApplicationViewState {
    currentTest: string;
}
export declare class TestApplicationView extends React.Component<{}, TestApplicationViewState> {
    state: TestApplicationViewState;
    getDefaultState(): TestApplicationViewState;
    render(): JSX.Element;
}
export declare class TestApplication {
    initialize(config: CharticulatorCoreConfig, containerID: string): Promise<void>;
}
