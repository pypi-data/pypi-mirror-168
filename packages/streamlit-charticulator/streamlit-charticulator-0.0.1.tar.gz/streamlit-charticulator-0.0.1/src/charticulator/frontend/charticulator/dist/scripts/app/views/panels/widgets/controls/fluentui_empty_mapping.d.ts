/// <reference types="react" />
import { Prototypes, Specification } from "../../../../../core";
interface EmptyMappingProps {
    renderColorPicker: () => JSX.Element;
    onClick: () => void;
    options: Prototypes.Controls.MappingEditorOptions;
    type: Specification.AttributeType;
}
export declare const EmptyMapping: ({ renderColorPicker, onClick, options, type, }: EmptyMappingProps) => JSX.Element;
interface EmptyColorButtonProps {
    onClick: () => void;
    styles?: {
        marginTop?: string;
    };
}
export declare const EmptyColorButton: ({ onClick, styles, }: EmptyColorButtonProps) => JSX.Element;
export {};
