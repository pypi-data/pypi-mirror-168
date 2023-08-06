import * as React from "react";
import { CSSProperties } from "react";
export interface InputNumberProps {
    defaultValue?: number;
    placeholder?: string;
    onEnter?: (value: number) => boolean;
    digits?: number;
    minimum?: number;
    maximum?: number;
    percentage?: boolean;
    step?: number;
    showSlider?: boolean;
    sliderRange?: [number, number];
    sliderFunction?: "linear" | "sqrt";
    showUpdown?: boolean;
    updownTick?: number;
    updownRange?: [number, number];
    updownStyle?: "normal" | "font";
    label?: string;
    stopPropagation?: boolean;
    styles?: CSSProperties;
}
export declare const FluentInputNumber: React.FC<InputNumberProps>;
