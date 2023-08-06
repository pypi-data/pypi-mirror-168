/// <reference types="react" />
import { AppStore } from "../stores";
import { ContextedComponent } from "../context_component";
import { Element } from "../../core/specification";
export declare class MessagePanel extends ContextedComponent<{
    store: AppStore;
}, Record<string, never>> {
    mappingButton: Element;
    private tokens;
    componentDidMount(): void;
    componentWillUnmount(): void;
    renderUnexpectedState(message: string): JSX.Element;
    render(): any;
}
