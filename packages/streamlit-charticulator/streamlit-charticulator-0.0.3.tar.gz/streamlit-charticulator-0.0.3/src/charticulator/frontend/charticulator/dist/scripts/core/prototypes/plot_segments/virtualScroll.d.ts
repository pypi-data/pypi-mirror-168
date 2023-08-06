import * as React from "react";
import { ZoomInfo } from "../..";
import { AxisDataBindingType } from "../../specification/types";
export interface VirtualScrollBarPropertes {
    initialPosition: number;
    onScroll: (position: number) => void;
    x: number;
    y: number;
    width: number;
    height: number;
    handlerBarWidth: number;
    vertical: boolean;
    zoom: ZoomInfo;
    scrollBarRatio: number;
    windowSize: number;
    dataType: AxisDataBindingType;
}
export declare const VirtualScrollBar: React.FC<VirtualScrollBarPropertes>;
