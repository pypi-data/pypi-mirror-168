import * as React from "react";
import { CSSProperties } from "react";
import { EventSubscription, Point, Prototypes, Specification } from "../../../../core";
import { DragData } from "../../../actions";
import { DragContext, DragModifiers, Droppable } from "../../../controllers/drag_controller";
import { AppStore } from "../../../stores";
import { CharticulatorPropertyAccessors } from "./types";
import { InputFontComboboxOptions, InputTextOptions, SearchWrapperOptions } from "../../../../core/prototypes/controls";
import { EventManager, UIManagerListener } from "./observer";
export declare type OnEditMappingHandler = (attribute: string, mapping: Specification.Mapping) => void;
export declare type OnMapDataHandler = (attribute: string, data: DragData.DataExpression, hints: Prototypes.DataMappingHints) => void;
export declare type OnSetPropertyHandler = (property: string, field: string, value: Specification.AttributeValue) => void;
export declare class FluentUIWidgetManager implements Prototypes.Controls.WidgetManager, CharticulatorPropertyAccessors {
    store: AppStore;
    objectClass: Prototypes.ObjectClass;
    ignoreSearch: boolean;
    constructor(store: AppStore, objectClass: Prototypes.ObjectClass, ignoreSearch?: boolean);
    onMapDataHandler: OnMapDataHandler;
    onEditMappingHandler: OnEditMappingHandler;
    private director;
    eventManager: EventManager;
    eventListener: UIManagerListener;
    private getKeyFromProperty;
    searchInput(options?: InputTextOptions): JSX.Element;
    searchWrapper(options: SearchWrapperOptions, ...widgets: JSX.Element[]): JSX.Element;
    mappingEditor(name: string, attribute: string, options: Prototypes.Controls.MappingEditorOptions): JSX.Element;
    getAttributeMapping(attribute: string): Specification.Mapping;
    getPropertyValue(property: Prototypes.Controls.Property): Specification.AttributeValue;
    private getDateFormat;
    emitSetProperty(property: Prototypes.Controls.Property, value: Specification.AttributeValue): void;
    emitUpdateProperty(event: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>, property: Prototypes.Controls.Property, prevKey: string, newKey: string): void;
    inputFormat(property: Prototypes.Controls.Property, options?: Prototypes.Controls.InputFormatOptions): JSX.Element;
    inputNumber(property: Prototypes.Controls.Property, options?: Prototypes.Controls.InputNumberOptions): JSX.Element;
    inputDate(property: Prototypes.Controls.Property, options?: Prototypes.Controls.InputDateOptions): JSX.Element;
    inputText(property: Prototypes.Controls.Property, options: InputTextOptions): JSX.Element;
    inputFontFamily(property: Prototypes.Controls.Property, options: InputFontComboboxOptions): JSX.Element;
    inputComboBox(property: Prototypes.Controls.Property, options: Prototypes.Controls.InputComboboxOptions): JSX.Element;
    inputSelect(property: Prototypes.Controls.Property, options: Prototypes.Controls.InputSelectOptions): JSX.Element;
    inputBoolean(properties: Prototypes.Controls.Property | Prototypes.Controls.Property[], options: Prototypes.Controls.InputBooleanOptions): JSX.Element;
    private defaultNotification;
    inputExpression(property: Prototypes.Controls.Property, options?: Prototypes.Controls.InputExpressionOptions): JSX.Element;
    inputColor(property: Prototypes.Controls.Property, options: Prototypes.Controls.InputColorOptions): JSX.Element;
    inputColorGradient(property: Prototypes.Controls.Property, inline?: boolean): JSX.Element;
    inputImage(property: Prototypes.Controls.Property): JSX.Element;
    inputImageProperty(property: Prototypes.Controls.Property): JSX.Element;
    clearButton(property: Prototypes.Controls.Property, icon?: string, isHeader?: boolean, styles?: CSSProperties): JSX.Element;
    setButton(property: Prototypes.Controls.Property, value: Specification.AttributeValue, icon?: string, text?: string): JSX.Element;
    scaleEditor(attribute: string, text: string): JSX.Element;
    orderByWidget(property: Prototypes.Controls.Property, options: Prototypes.Controls.OrderWidgetOptions): JSX.Element;
    reorderWidget(property: Prototypes.Controls.Property, options?: Prototypes.Controls.ReOrderWidgetOptions): JSX.Element;
    arrayWidget(property: Prototypes.Controls.Property, renderItem: (item: Prototypes.Controls.Property) => JSX.Element, options?: Prototypes.Controls.ArrayWidgetOptions): JSX.Element;
    dropTarget(options: Prototypes.Controls.DropTargetOptions, widget: JSX.Element): JSX.Element;
    icon(icon: string): JSX.Element;
    label(title: string, options?: Prototypes.Controls.LabelOptions): JSX.Element;
    text(title: string, align?: "left" | "center" | "right"): JSX.Element;
    sep(): JSX.Element;
    sectionHeader(title: string, widget?: JSX.Element, options?: Prototypes.Controls.RowOptions): JSX.Element;
    horizontal(cols: number[], ...widgets: JSX.Element[]): JSX.Element;
    styledHorizontal(styles: CSSProperties, cols: number[], ...widgets: JSX.Element[]): JSX.Element;
    filterEditor(options: Prototypes.Controls.FilterEditorOptions): JSX.Element;
    groupByEditor(options: Prototypes.Controls.GroupByEditorOptions): JSX.Element;
    nestedChartEditor(property: Prototypes.Controls.Property, options: Prototypes.Controls.NestedChartEditorOptions): JSX.Element;
    row(title?: string, widget?: JSX.Element): JSX.Element;
    vertical(...widgets: JSX.Element[]): JSX.Element;
    styledVertical(styles: CSSProperties, ...widgets: JSX.Element[]): JSX.Element;
    verticalGroup(options: Prototypes.Controls.VerticalGroupOptions, widgets: JSX.Element[]): JSX.Element;
    table(rows: JSX.Element[][]): JSX.Element;
    scrollList(widgets: Prototypes.Controls.Widget[], options?: Prototypes.Controls.ScrollListOptions): JSX.Element;
    tooltip(widget: JSX.Element, tooltipContent: JSX.Element): JSX.Element;
    customCollapsiblePanel(widgets: JSX.Element[], options?: Prototypes.Controls.CustomCollapsiblePanelOptions): JSX.Element;
    reorderByAnotherColumnWidget(property: Prototypes.Controls.Property, options?: Prototypes.Controls.ReOrderWidgetOptions): JSX.Element;
    shouldDrawComponent(options: string[]): boolean;
}
export interface DropZoneViewProps {
    /** Determine whether the data is acceptable */
    filter: (x: any) => boolean;
    /** The user dropped the thing */
    onDrop: (data: any, point: Point, modifiers: DragModifiers) => void;
    /** className of the root div element */
    className: string;
    onClick?: () => void;
    /** Display this instead when dragging (normally we show what's in this view) */
    draggingHint?: () => JSX.Element;
}
export interface DropZoneViewState {
    isInSession: boolean;
    isDraggingOver: boolean;
    data: any;
}
export declare class DropZoneView extends React.Component<DropZoneViewProps, DropZoneViewState> implements Droppable {
    dropContainer: HTMLDivElement;
    tokens: EventSubscription[];
    constructor(props: DropZoneViewProps);
    componentDidMount(): void;
    componentWillUnmount(): void;
    onDragEnter(ctx: DragContext): boolean;
    render(): JSX.Element;
}
export declare class FluentDetailsButton extends React.Component<{
    widgets: JSX.Element[];
    manager: Prototypes.Controls.WidgetManager;
    label?: string;
}, Record<string, unknown>> {
    inner: DetailsButtonInner;
    componentDidUpdate(): void;
    render(): JSX.Element;
}
export declare class DetailsButtonInner extends React.Component<{
    parent: FluentDetailsButton;
}, Record<string, unknown>> {
    render(): JSX.Element;
}
