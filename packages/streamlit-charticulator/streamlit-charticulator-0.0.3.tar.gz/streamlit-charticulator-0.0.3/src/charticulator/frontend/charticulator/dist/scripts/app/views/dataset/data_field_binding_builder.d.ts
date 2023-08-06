import { DataFieldSelectorValue } from "./fluent_ui_data_field_selector";
import { Dataset } from "../../../core";
import { AppStore } from "../../stores";
import { IContextualMenuItem, IContextualMenuListProps, IRenderFunction } from "@fluentui/react";
import { FluentMappingEditor } from "../panels/widgets/fluent_mapping_editor";
import { MappingType } from "../../../core/specification";
export interface IDefaultValue {
    table: string;
    expression?: string;
    type?: MappingType;
}
interface Builder {
    /**
     * Description for null element
     * @default (none)
     */
    produceNullDescription(nullDescription: string): void;
    /**
     * Add onChange function for menu items
     */
    produceOnChange(fn: (value: DataFieldSelectorValue) => void): void;
    /**
     * Use Aggregation
     */
    produceUsingAggregation(useAggregation: boolean): void;
    /**
     * Show fields only from a particular table
     * Show fields only of certain kinds or types (categorical / numerical)
     */
    produceFields(datasetStore: AppStore, table?: string, kinds?: Dataset.DataKind[], types?: Dataset.DataType[]): void;
    /**
     * Add default value
     */
    produceDefaultValue(dafaultValue: IDefaultValue): void;
    getMenuItems(): IContextualMenuItem[];
    produceScaleEditor(store: AppStore, attribute: string, parent: FluentMappingEditor): void;
    buildMenu(): void;
    /**
     * Add additional derived columns
     * @see type2DerivedColumns
     */
    produceDerivedColumns(): void;
}
export declare class MenuItemBuilder implements Builder {
    private menuItemsCreator;
    constructor();
    produceScaleEditor(store: AppStore, attribute: string, parent: FluentMappingEditor): void;
    produceDerivedColumns(): void;
    produceOnChange(fn: (value: DataFieldSelectorValue) => void): void;
    getMenuItems(): IContextualMenuItem[];
    reset(): void;
    produceNullDescription(nullDescription: string): void;
    produceUsingAggregation(useAggregation: boolean): void;
    produceFields(datasetStore: AppStore, table?: string, kinds?: Dataset.DataKind[], types?: Dataset.DataType[]): void;
    produceDefaultValue(dafaultValue: IDefaultValue): void;
    buildMenu(): void;
}
export declare class Director {
    private builder;
    setBuilder(builder: Builder): void;
    buildNullMenu(): IContextualMenuItem[];
    buildFieldsMenu(onClick: (value: DataFieldSelectorValue) => void, defaultValue: IDefaultValue, datasetStore: AppStore, parent: FluentMappingEditor, attribute: string, table?: string, kinds?: Dataset.DataKind[], types?: Dataset.DataType[]): IContextualMenuItem[];
    buildSectionHeaderFieldsMenu(onClick: (value: DataFieldSelectorValue) => void, defaultValue: IDefaultValue, datasetStore: AppStore, table?: string, kinds?: Dataset.DataKind[], types?: Dataset.DataType[]): IContextualMenuItem[];
    getMenuRender(): IRenderFunction<IContextualMenuListProps>;
}
export {};
