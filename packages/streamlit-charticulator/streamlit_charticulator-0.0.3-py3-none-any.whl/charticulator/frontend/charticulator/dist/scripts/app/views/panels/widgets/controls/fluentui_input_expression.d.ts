import * as React from "react";
import { Expression } from "../../../../../core";
export interface InputExpressionProps {
    validate?: (value: string) => Expression.VerifyUserExpressionReport;
    defaultValue?: string;
    value?: string;
    placeholder?: string;
    onEnter?: (value: string) => boolean;
    onCancel?: () => void;
    textExpression?: boolean;
    allowNull?: boolean;
    label?: string;
    stopPropagation?: boolean;
}
export interface InputExpressionState {
    errorMessage?: string;
    errorIndicator: boolean;
    value?: string;
}
export declare const FluentInputExpression: React.FC<InputExpressionProps>;
