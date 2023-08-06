import * as React from "react";
import { Expression } from "../../../../../core";
import { InputExpressionProps } from "./fluentui_input_expression";
export interface InputFormatProps {
    validate?: (value: string) => Expression.VerifyUserExpressionReport;
    defaultValue?: string;
    placeholder?: string;
    onEnter?: (value: string) => boolean;
    onCancel?: () => void;
    textExpression?: boolean;
    allowNull?: boolean;
}
export interface InputFormatState {
    errorMessage?: string;
    errorIndicator: boolean;
    value?: string;
}
export declare const FluentInputFormat: React.FC<InputExpressionProps>;
