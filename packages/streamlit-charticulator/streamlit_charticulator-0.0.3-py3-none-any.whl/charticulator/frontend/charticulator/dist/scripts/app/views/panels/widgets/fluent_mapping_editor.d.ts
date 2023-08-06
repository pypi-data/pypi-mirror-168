import * as React from "react";
import { EventEmitter, Prototypes, Specification } from "../../../../core";
import { DragData } from "../../../actions";
import { ContextedComponent } from "../../../context_component";
import { CharticulatorPropertyAccessors } from "./types";
import { AppStore } from "../../../stores";
import { ObjectClass } from "../../../../core/prototypes";
import { Director } from "../../dataset/data_field_binding_builder";
export interface MappingEditorProps {
    parent: Prototypes.Controls.WidgetManager & CharticulatorPropertyAccessors;
    attribute: string;
    type: Specification.AttributeType;
    options: Prototypes.Controls.MappingEditorOptions;
    store?: AppStore;
}
export interface MappingEditorState {
    showNoneAsValue: boolean;
    isDataFieldValueSelectionOpen: boolean;
    isColorPickerOpen: boolean;
}
export declare class FluentMappingEditor extends React.Component<MappingEditorProps, MappingEditorState> {
    mappingButton: HTMLElement;
    noneLabel: HTMLSpanElement;
    scaleMappingDisplay: HTMLSpanElement;
    updateEvents: EventEmitter;
    state: MappingEditorState;
    director: Director;
    private changeDataFieldValueSelectionState;
    private changeColorPickerState;
    private openDataFieldValueSelection;
    private initiateValueEditor;
    private setValueMapping;
    clearMapping(): void;
    mapData(data: DragData.DataExpression, hints: Prototypes.DataMappingHints): void;
    componentDidUpdate(): void;
    getTableOrDefault(): string;
    constructor(props: MappingEditorProps);
    private renderValueEditor;
    private renderColorPicker;
    private renderCurrentAttributeMapping;
    render(): JSX.Element;
    static menuKeyClick(derivedExpression: string): void;
    static openEditor(expressionString: string, clickOnButton: boolean, mappingButton: HTMLElement): void;
}
export interface DataMappAndScaleEditorProps {
    attribute: string;
    defaultMapping: Specification.Mapping;
    options: Prototypes.Controls.MappingEditorOptions;
    parent: FluentMappingEditor;
    onClose: () => void;
    alignLeft?: boolean;
    plotSegment: ObjectClass;
}
export interface DataMappAndScaleEditorState {
    currentMapping: Specification.Mapping;
}
export declare class DataMappAndScaleEditor extends ContextedComponent<DataMappAndScaleEditorProps, DataMappAndScaleEditorState> {
    state: {
        currentMapping: Specification.Mapping;
    };
    private tokens;
    componentDidMount(): void;
    componentWillUnmount(): void;
    renderScaleEditor(): JSX.Element;
    renderDataPicker(): JSX.Element;
    render(): JSX.Element;
}
export declare function parentOfType(p: ObjectClass, typeSought: string): Prototypes.ObjectClass<Specification.AttributeMap, Specification.AttributeMap>;
