import * as React from "react";
import { Prototypes, ZoomInfo } from "../../../../core";
import { HandlesDragContext } from "./common";
export interface HandlesViewProps {
    zoom: ZoomInfo;
    active?: boolean;
    visible?: boolean;
    handles: Prototypes.Handles.Description[];
    isAttributeSnapped?: (attribute: string) => boolean;
    onDragStart?: (handle: Prototypes.Handles.Description, ctx: HandlesDragContext) => void;
}
export declare class HandlesView extends React.Component<HandlesViewProps, Record<string, unknown>> {
    renderHandle(handle: Prototypes.Handles.Description): JSX.Element;
    render(): JSX.Element;
}
