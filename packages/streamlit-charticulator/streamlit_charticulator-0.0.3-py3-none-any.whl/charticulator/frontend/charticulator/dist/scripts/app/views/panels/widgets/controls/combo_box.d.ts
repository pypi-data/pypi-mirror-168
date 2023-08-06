import * as React from "react";
export interface ComboBoxFontFamilyProps {
    defaultValue: string;
    label?: string;
    onEnter?: (value: string) => boolean;
    onCancel?: () => void;
}
export declare const FluentComboBoxFontFamily: React.FC<ComboBoxFontFamilyProps>;
