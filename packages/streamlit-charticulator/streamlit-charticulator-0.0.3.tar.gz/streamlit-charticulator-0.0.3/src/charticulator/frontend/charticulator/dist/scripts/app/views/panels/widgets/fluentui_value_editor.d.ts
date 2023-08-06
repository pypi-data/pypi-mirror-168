/// <reference types="react" />
import { IContextualMenuItem, IContextualMenuListProps, IRenderFunction } from "@fluentui/react";
import { Specification } from "../../../../core";
import { DataMappingHints } from "../../../../core/prototypes";
import { InputNumberOptions } from "../../../../core/prototypes/controls";
import { ContextedComponent } from "../../../context_component";
export interface ValueEditorProps {
    value: Specification.AttributeValue;
    type: Specification.AttributeType;
    label?: string;
    /** When value is null, show defaultValue in editor */
    defaultValue?: Specification.AttributeValue;
    /** When value is null, show placeholder text */
    placeholder?: string;
    onEmitValue?: (value: Specification.AttributeValue) => void;
    onClear?: () => void;
    /** In some cases the value editor can emit data mapping */
    onEmitMapping?: (mapping: Specification.Mapping) => void;
    onBeginDataFieldSelection?: (anchor?: Element) => void;
    /** The table to use for data mapping */
    getTable?: () => string;
    hints?: DataMappingHints;
    numberOptions?: InputNumberOptions;
    stopPropagation?: boolean;
    mainMenuItems?: IContextualMenuItem[];
    menuRender: IRenderFunction<IContextualMenuListProps>;
}
interface ValueEditorState {
    value: string;
    open: boolean;
}
export declare class FluentValueEditor extends ContextedComponent<ValueEditorProps, ValueEditorState> {
    emitClearValue(): void;
    state: ValueEditorState;
    emitSetValue(value: Specification.AttributeValue): void;
    emitMapping(mapping: Specification.Mapping): void;
    componentWillReceiveProps(nextProps: Readonly<ValueEditorProps>): void;
    render(): JSX.Element;
}
export {};
