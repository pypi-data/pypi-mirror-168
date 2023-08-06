"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
Object.defineProperty(exports, "__esModule", { value: true });
exports.symbolTypesList = exports.MarkClass = exports.registerClasses = void 0;
/**
 * # Marks
 *
 * Most of mark elements extends {@link EmphasizableMarkClass} and  {@link MarkClass} clases.
 *
 * Each mark has a property
 *
 * ```typescript
 * public readonly object: Specification.Element<PropertiesType>;
 * ```
 *
 * it's a single graphical mark, such as rectangle, circle, wedge; an element is driven by a group of data rows.
 *
 * For example, char in the sample has one rectangle in the glyph. But if the chart has several glyphs, rectangle mark has several objects with different properties (different height).
 *
 * ![Mark class and object](media://mark_class_objects.png)
 *
 * The main interface of the object is {@linkcode ObjectClass}
 *
 * The interface contains several properties:
 *
 * ```typescript
 *   export interface Object<
 *      PropertiesType extends ObjectProperties = ObjectProperties
 *    > extends Identifiable {
 *      classID: string;
 *      properties: PropertiesType;
 *      mappings: Mappings;
 * }
 * ```
 *
 * classID - each mark class has its own ID, you can find them in ts files of marks. For example, [image](image.ts#L39) mark class has:
 *
 * ```typescript
 * public static classID = "mark.image";
 * ```
 *
 * properties - is attributes of objects. Read more about difference of properties and attributes in {@link "core/index"} module documentation.
 *
 *
 * All marks implement several methods of {@link ObjectClass}
 * for exmaple
 * `{@link ObjectClass.getAttributePanelWidgets}` - the method responsible for displaying widgets in the property panel. Each time when a user selects the mark in the object browser, the charticualtor calls this method to display properties. Charticulator displays the properties for rectangle named `Shape1`
 *
 * ![Mark widgets](media://mark_widgets.png)
 *
 * {@link ObjectClass.getTemplateParameters} - returns configurable parameters of the object. This method calls in {@link ChartTemplateBuilder.addObject} method to collect all parameters into inference list
 *
 * @packageDocumentation
 * @preferred
 */
var object_1 = require("../object");
var mark_1 = require("./mark");
Object.defineProperty(exports, "MarkClass", { enumerable: true, get: function () { return mark_1.MarkClass; } });
var anchor_1 = require("./anchor");
var data_axis_1 = require("./data_axis");
var image_1 = require("./image");
var line_1 = require("./line");
var nested_chart_1 = require("./nested_chart");
var rect_1 = require("./rect");
var symbol_1 = require("./symbol");
Object.defineProperty(exports, "symbolTypesList", { enumerable: true, get: function () { return symbol_1.symbolTypesList; } });
var text_1 = require("./text");
var icon_1 = require("./icon");
var textbox_1 = require("./textbox");
function registerClasses() {
    object_1.ObjectClasses.Register(anchor_1.AnchorElement);
    object_1.ObjectClasses.Register(rect_1.RectElementClass);
    object_1.ObjectClasses.Register(line_1.LineElementClass);
    object_1.ObjectClasses.Register(symbol_1.SymbolElementClass);
    object_1.ObjectClasses.Register(text_1.TextElementClass);
    object_1.ObjectClasses.Register(textbox_1.TextboxElementClass);
    object_1.ObjectClasses.Register(image_1.ImageElementClass);
    object_1.ObjectClasses.Register(icon_1.IconElementClass);
    object_1.ObjectClasses.Register(nested_chart_1.NestedChartElementClass);
    object_1.ObjectClasses.Register(data_axis_1.DataAxisClass);
}
exports.registerClasses = registerClasses;
//# sourceMappingURL=index.js.map