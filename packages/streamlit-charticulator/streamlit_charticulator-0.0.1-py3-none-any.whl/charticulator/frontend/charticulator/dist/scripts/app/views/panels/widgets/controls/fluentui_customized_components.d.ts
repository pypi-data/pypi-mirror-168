import { IButtonStyles, IDropdownProps, IGroupedListStyleProps, IGroupedListStyles, IGroupHeaderStyleProps, IGroupHeaderStyles, ILabelStyles, IRenderFunction, IStyleFunctionOrObject, ITextFieldProps } from "@fluentui/react";
export declare const defultBindButtonSize: {
    height: string;
    width: string;
};
export declare const FluentButton: import("styled-components").StyledComponent<"div", any, {
    marginTop?: string;
    marginLeft?: string;
    paddingRight?: string;
}, never>;
export declare const FluentLabelHeader: import("styled-components").StyledComponent<"div", any, {
    marginBottom?: string;
    marginTop?: string;
    marginRight?: string;
}, never>;
export declare const FluentActionButton: import("styled-components").StyledComponent<"div", any, {}, never>;
export declare const FluentTextField: import("styled-components").StyledComponent<"div", any, {}, never>;
export declare const FluentCheckbox: import("styled-components").StyledComponent<"div", any, {}, never>;
export declare const FluentRowLayout: import("styled-components").StyledComponent<"div", any, {}, never>;
export declare const FluentDataBindingMenuItem: import("styled-components").StyledComponent<"div", any, {
    backgroundColor?: string;
    backgroundColorHover?: string;
}, never>;
export declare const FluentDataBindingMenuLabel: import("styled-components").StyledComponent<"div", any, {}, never>;
export declare const FluentColumnLayout: import("styled-components").StyledComponent<"div", any, {}, never>;
export declare const FluentLayoutItem: import("styled-components").StyledComponent<"div", any, {
    flex: number;
}, never>;
export declare const defaultFontWeight = 400;
export declare const defaultLabelStyle: ILabelStyles;
export declare const labelRender: IRenderFunction<ITextFieldProps & IDropdownProps>;
export declare const NestedChartButtonsWrapper: import("styled-components").StyledComponent<"div", any, {}, never>;
export declare const FluentGroupedList: import("styled-components").StyledComponent<"div", any, {
    marginLeft?: number;
}, never>;
export declare const defultComponentsHeight: {
    height: string;
    lineHeight: string;
};
export declare const groupHeaderStyles: IStyleFunctionOrObject<IGroupHeaderStyleProps, IGroupHeaderStyles>;
export declare const groupStyles: IStyleFunctionOrObject<IGroupedListStyleProps, IGroupedListStyles>;
export declare const PlaceholderStyle: import("styled-components").StyledComponent<"div", any, {
    color?: string;
}, never>;
export declare const FluentDropdown: import("styled-components").StyledComponent<"div", any, {}, never>;
export declare const FluentDropdownWrapper: import("styled-components").StyledComponent<"div", any, {}, never>;
export declare const FluentDatePickerWrapper: import("styled-components").StyledComponent<"div", any, {}, never>;
export declare const defaultStyle: any;
export declare const PanelHeaderStyles: Partial<IButtonStyles>;
