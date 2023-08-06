import { IButtonStyles, IDropdownStyles, ILabelStyles, ITextFieldStyles } from "@fluentui/react";
export declare const defaultActionButtonsStyles: IButtonStyles;
export declare const colorPalettesLabelStyles: ILabelStyles;
export declare const deleteColorStyles: IButtonStyles;
export declare const dropdownStyles: Partial<IDropdownStyles>;
export declare const colorTextInputStyles: Partial<ITextFieldStyles>;
export declare const PalettesWrapper: import("styled-components").StyledComponent<"div", any, {}, never>;
export declare const TabWrapper: import("styled-components").StyledComponent<"div", any, {}, never>;
export declare const ColorRowWrapper: import("styled-components").StyledComponent<"div", any, {}, never>;
interface ColorCellProps {
    $color: string;
}
export declare const ColorCell: import("styled-components").StyledComponent<"span", any, ColorCellProps, never>;
export declare const ColorGradientWrapper: import("styled-components").StyledComponent<"span", any, {}, never>;
export declare const CustomGradientButtonsWrapper: import("styled-components").StyledComponent<"div", any, {}, never>;
export {};
