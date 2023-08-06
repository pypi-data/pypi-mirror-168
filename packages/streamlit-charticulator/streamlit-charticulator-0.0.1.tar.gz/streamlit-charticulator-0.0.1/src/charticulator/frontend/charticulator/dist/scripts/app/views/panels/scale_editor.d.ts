import * as React from "react";
import { EventSubscription, Specification } from "../../../core";
import { AppStore } from "../../stores";
import { ObjectClass } from "../../../core/prototypes";
export interface ScaleEditorProps {
    scale: Specification.Scale;
    scaleMapping: Specification.ScaleMapping;
    store: AppStore;
    plotSegment: ObjectClass;
}
export declare class ScaleEditor extends React.Component<ScaleEditorProps, Record<string, unknown>> {
    token: EventSubscription;
    componentDidMount(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
}
