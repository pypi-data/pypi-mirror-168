/// <reference types="react" />
import { ContextedComponent } from "../../context_component";
export interface LegendCreationPanelProps {
    onFinish?: () => void;
}
export interface LegendCreationPanelState {
    legendDataSource: "columnNames" | "columnValues";
    legendType: "color" | "numerical" | "categorical";
    errorReport: string;
}
export declare class LegendCreationPanel extends ContextedComponent<LegendCreationPanelProps, LegendCreationPanelState> {
    state: LegendCreationPanelState;
    private groupBySelector;
    private getDefaultState;
    render(): JSX.Element;
}
