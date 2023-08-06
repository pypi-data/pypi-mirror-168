import { Controls } from "../common";
import { Dataset, Specification } from "../../index";
import { CharticulatorPropertyAccessors } from "../../../app/views/panels/widgets/types";
import { AxisDataBinding } from "../../../core/specification/types";
export declare function getTableColumns(manager: Controls.WidgetManager & CharticulatorPropertyAccessors): Dataset.Column[];
export declare function getColumnByExpression(manager: Controls.WidgetManager & CharticulatorPropertyAccessors, expression: string): Dataset.Column[];
export declare function getColumnNameByExpression(expression: string): string;
export declare function parseDerivedColumnsExpression(expression: string): string;
export declare function transformOrderByExpression(expression: string): string;
export declare function shouldShowTickFormatForTickExpression(data: Specification.Types.AxisDataBinding, manager: Controls.WidgetManager): boolean;
export declare type CategoryItemsWithId = [unknown[], number];
export declare type CategoryItemsWithIds = CategoryItemsWithId[];
export declare const JoinSymbol = ", ";
/**
 * Transform data to sting array
 * [
 * [[data], id],
 * [....]
 * ]
 * @param itemsWithIds
 * @return unique string array
 */
export declare function transformOnResetCategories(itemsWithIds: CategoryItemsWithIds): string[];
export declare function getOnConfirmFunction(datasetAxisData: any[][], items: string[], itemsWithIds: CategoryItemsWithIds, data: AxisDataBinding): void;
export declare function transformDataToCategoryItemsWithIds(data: unknown[][]): CategoryItemsWithIds;
export declare function updateWidgetCategoriesByExpression(widgetData: unknown[][]): string[];
export declare function getSortedCategories(itemsWithIds: CategoryItemsWithIds): string[];
