/// <reference types="react" />
import { AppStore } from "../../stores";
import { ContextedComponent } from "../../context_component";
import { Element } from "../../../core/specification";
export declare class ScalesPanel extends ContextedComponent<{
    store: AppStore;
}, {
    isSelected: string;
}> {
    mappingButton: Element;
    private tokens;
    constructor(props: {
        store: AppStore;
    });
    componentDidMount(): void;
    componentWillUnmount(): void;
    renderUnexpectedState(message: string): JSX.Element;
    private getPropertyDisplayName;
    render(): any;
}
