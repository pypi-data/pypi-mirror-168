import { IDropdownOption, IDropdownStyles } from "@fluentui/react";
import { Prototypes } from "../../../../core";
import { CSSProperties } from "react";
export declare const dropdownStyles: (options: Prototypes.Controls.InputSelectOptions) => Partial<IDropdownStyles>;
export declare const iconStyles: CSSProperties;
export declare const onRenderOption: (option: IDropdownOption) => JSX.Element;
export declare const onRenderTitle: (options: IDropdownOption[]) => JSX.Element;
