"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.ExpandOrCollapsePanelsUpdated = exports.SearchUpdated = exports.OpenNestedEditor = exports.ClearMessages = exports.RemoveMessage = exports.AddMessage = exports.SetCurrentTool = exports.SetCurrentMappingAttribute = exports.FocusToMarkAttribute = exports.SelectChartElement = exports.SelectGlyph = exports.ReorderGlyphMark = exports.ReorderChartElement = exports.ExtendPlotSegment = exports.SetObjectMappingScale = exports.DeleteObjectProperty = exports.SetObjectProperty = exports.SetChartAttribute = exports.SetChartSize = exports.UpdateChartAttribute = exports.AddLinks = exports.BindDataToAxis = exports.SnapChartElements = exports.UpdateChartElementAttribute = exports.ToggleLegendForScale = exports.SetScaleAttribute = exports.SetPlotSegmentGroupBy = exports.SetPlotSegmentFilter = exports.MapDataToChartElementAttribute = exports.SetChartElementMapping = exports.DeleteChartElement = exports.AddChartElement = exports.UpdateGlyphAttribute = exports.SetGlyphAttribute = exports.MarkActionGroup = exports.SnapMarks = exports.UpdateMarkAttribute = exports.UnmapMarkAttribute = exports.SetMarkAttribute = exports.MarkAction = exports.MapDataToMarkAttribute = exports.RemoveMarkFromGlyph = exports.AddMarkToGlyph = exports.RemoveGlyph = exports.AddGlyph = exports.ConvertColumnDataType = exports.UpdateDataAxis = exports.UpdatePlotSegments = exports.ReplaceDataset = exports.ImportChartAndDataset = exports.ImportDataset = exports.Load = exports.SaveAs = exports.Save = exports.Open = exports.SaveExportTemplatePropertyName = exports.ExportTemplate = exports.Export = exports.Reset = exports.Redo = exports.Undo = exports.ClearSelection = exports.SelectMark = exports.Action = void 0;
var core_1 = require("../../core");
Object.defineProperty(exports, "Action", { enumerable: true, get: function () { return core_1.Action; } });
Object.defineProperty(exports, "SelectMark", { enumerable: true, get: function () { return core_1.SelectMark; } });
Object.defineProperty(exports, "ClearSelection", { enumerable: true, get: function () { return core_1.ClearSelection; } });
var Undo = /** @class */ (function (_super) {
    __extends(Undo, _super);
    function Undo() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Undo.prototype.digest = function () {
        return { name: "Undo" };
    };
    return Undo;
}(core_1.Action));
exports.Undo = Undo;
var Redo = /** @class */ (function (_super) {
    __extends(Redo, _super);
    function Redo() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Redo.prototype.digest = function () {
        return { name: "Redo" };
    };
    return Redo;
}(core_1.Action));
exports.Redo = Redo;
var Reset = /** @class */ (function (_super) {
    __extends(Reset, _super);
    function Reset() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Reset.prototype.digest = function () {
        return { name: "Reset" };
    };
    return Reset;
}(core_1.Action));
exports.Reset = Reset;
var Export = /** @class */ (function (_super) {
    __extends(Export, _super);
    function Export(type, options) {
        if (options === void 0) { options = {}; }
        var _this = _super.call(this) || this;
        _this.type = type;
        _this.options = options;
        return _this;
    }
    Export.prototype.digest = function () {
        return { name: "Export", type: this.type, options: this.options };
    };
    return Export;
}(core_1.Action));
exports.Export = Export;
var ExportTemplate = /** @class */ (function (_super) {
    __extends(ExportTemplate, _super);
    function ExportTemplate(kind, target, properties) {
        var _this = _super.call(this) || this;
        _this.kind = kind;
        _this.target = target;
        _this.properties = properties;
        return _this;
    }
    ExportTemplate.prototype.digest = function () {
        return { name: "ExportTemplate" };
    };
    return ExportTemplate;
}(core_1.Action));
exports.ExportTemplate = ExportTemplate;
var SaveExportTemplatePropertyName = /** @class */ (function (_super) {
    __extends(SaveExportTemplatePropertyName, _super);
    function SaveExportTemplatePropertyName(objectId, propertyName, value) {
        var _this = _super.call(this) || this;
        _this.objectId = objectId;
        _this.propertyName = propertyName;
        _this.value = value;
        return _this;
    }
    SaveExportTemplatePropertyName.prototype.digest = function () {
        return { name: "SaveExportTemplatePropertyName" };
    };
    return SaveExportTemplatePropertyName;
}(core_1.Action));
exports.SaveExportTemplatePropertyName = SaveExportTemplatePropertyName;
var Open = /** @class */ (function (_super) {
    __extends(Open, _super);
    function Open(id, onFinish) {
        var _this = _super.call(this) || this;
        _this.id = id;
        _this.onFinish = onFinish;
        return _this;
    }
    Open.prototype.digest = function () {
        return { name: "Open", id: this.id };
    };
    return Open;
}(core_1.Action));
exports.Open = Open;
/** Save the current chart */
var Save = /** @class */ (function (_super) {
    __extends(Save, _super);
    function Save(onFinish) {
        var _this = _super.call(this) || this;
        _this.onFinish = onFinish;
        return _this;
    }
    Save.prototype.digest = function () {
        return { name: "Save" };
    };
    return Save;
}(core_1.Action));
exports.Save = Save;
var SaveAs = /** @class */ (function (_super) {
    __extends(SaveAs, _super);
    function SaveAs(saveAs, onFinish) {
        var _this = _super.call(this) || this;
        _this.saveAs = saveAs;
        _this.onFinish = onFinish;
        return _this;
    }
    SaveAs.prototype.digest = function () {
        return { name: "SaveAs", saveAs: this.saveAs };
    };
    return SaveAs;
}(core_1.Action));
exports.SaveAs = SaveAs;
var Load = /** @class */ (function (_super) {
    __extends(Load, _super);
    function Load(projectData) {
        var _this = _super.call(this) || this;
        _this.projectData = projectData;
        return _this;
    }
    Load.prototype.digest = function () {
        return { name: "Load" };
    };
    return Load;
}(core_1.Action));
exports.Load = Load;
var ImportDataset = /** @class */ (function (_super) {
    __extends(ImportDataset, _super);
    function ImportDataset(dataset) {
        var _this = _super.call(this) || this;
        _this.dataset = dataset;
        return _this;
    }
    ImportDataset.prototype.digest = function () {
        return { name: "ImportDataset", datasetName: this.dataset.name };
    };
    return ImportDataset;
}(core_1.Action));
exports.ImportDataset = ImportDataset;
var ImportChartAndDataset = /** @class */ (function (_super) {
    __extends(ImportChartAndDataset, _super);
    function ImportChartAndDataset(specification, dataset, options, originSpecification) {
        var _this = _super.call(this) || this;
        _this.specification = specification;
        _this.dataset = dataset;
        _this.options = options;
        _this.originSpecification = originSpecification;
        return _this;
    }
    ImportChartAndDataset.prototype.digest = function () {
        return { name: "ImportChartAndDataset" };
    };
    return ImportChartAndDataset;
}(core_1.Action));
exports.ImportChartAndDataset = ImportChartAndDataset;
var ReplaceDataset = /** @class */ (function (_super) {
    __extends(ReplaceDataset, _super);
    function ReplaceDataset(dataset, keepState) {
        if (keepState === void 0) { keepState = false; }
        var _this = _super.call(this) || this;
        _this.dataset = dataset;
        _this.keepState = keepState;
        return _this;
    }
    ReplaceDataset.prototype.digest = function () {
        return {
            name: "ReplaceDataset",
            datasetName: this.dataset.name,
            keepState: this.keepState,
        };
    };
    return ReplaceDataset;
}(core_1.Action));
exports.ReplaceDataset = ReplaceDataset;
/** Invokes updaes all plot segments on the chart,  */
var UpdatePlotSegments = /** @class */ (function (_super) {
    __extends(UpdatePlotSegments, _super);
    function UpdatePlotSegments() {
        return _super.call(this) || this;
    }
    UpdatePlotSegments.prototype.digest = function () {
        return { name: "UpdatePlotSegments" };
    };
    return UpdatePlotSegments;
}(core_1.Action));
exports.UpdatePlotSegments = UpdatePlotSegments;
var UpdateDataAxis = /** @class */ (function (_super) {
    __extends(UpdateDataAxis, _super);
    function UpdateDataAxis() {
        return _super.call(this) || this;
    }
    UpdateDataAxis.prototype.digest = function () {
        return { name: "UpdateDataAxis" };
    };
    return UpdateDataAxis;
}(core_1.Action));
exports.UpdateDataAxis = UpdateDataAxis;
var ConvertColumnDataType = /** @class */ (function (_super) {
    __extends(ConvertColumnDataType, _super);
    function ConvertColumnDataType(tableName, column, type) {
        var _this = _super.call(this) || this;
        _this.tableName = tableName;
        _this.column = column;
        _this.type = type;
        return _this;
    }
    ConvertColumnDataType.prototype.digest = function () {
        return { name: "ConvertColumnDataType" };
    };
    return ConvertColumnDataType;
}(core_1.Action));
exports.ConvertColumnDataType = ConvertColumnDataType;
// Glyph editing actions
/** Add an empty glyph to the chart */
var AddGlyph = /** @class */ (function (_super) {
    __extends(AddGlyph, _super);
    function AddGlyph(classID) {
        var _this = _super.call(this) || this;
        _this.classID = classID;
        return _this;
    }
    AddGlyph.prototype.digest = function () {
        return {
            name: "AddGlyph",
            classID: this.classID,
        };
    };
    return AddGlyph;
}(core_1.Action));
exports.AddGlyph = AddGlyph;
/** Remove a glyph from the chart */
var RemoveGlyph = /** @class */ (function (_super) {
    __extends(RemoveGlyph, _super);
    function RemoveGlyph(glyph) {
        var _this = _super.call(this) || this;
        _this.glyph = glyph;
        return _this;
    }
    RemoveGlyph.prototype.digest = function () {
        return {
            name: "RemoveGlyph",
            glyph: core_1.objectDigest(this.glyph),
        };
    };
    return RemoveGlyph;
}(core_1.Action));
exports.RemoveGlyph = RemoveGlyph;
// Mark editing actions
/** Add an mark to the glyph */
var AddMarkToGlyph = /** @class */ (function (_super) {
    __extends(AddMarkToGlyph, _super);
    function AddMarkToGlyph(glyph, classID, point, mappings, properties) {
        if (mappings === void 0) { mappings = {}; }
        if (properties === void 0) { properties = {}; }
        var _this = _super.call(this) || this;
        _this.glyph = glyph;
        _this.classID = classID;
        _this.point = point;
        _this.mappings = mappings;
        _this.properties = properties;
        return _this;
    }
    AddMarkToGlyph.prototype.digest = function () {
        return {
            name: "AddMarkToGlyph",
            classID: this.classID,
            glyph: core_1.objectDigest(this.glyph),
            mappings: this.mappings,
            properties: this.properties,
        };
    };
    return AddMarkToGlyph;
}(core_1.Action));
exports.AddMarkToGlyph = AddMarkToGlyph;
/** Remove an mark from the glyph */
var RemoveMarkFromGlyph = /** @class */ (function (_super) {
    __extends(RemoveMarkFromGlyph, _super);
    function RemoveMarkFromGlyph(glyph, mark) {
        var _this = _super.call(this) || this;
        _this.glyph = glyph;
        _this.mark = mark;
        return _this;
    }
    RemoveMarkFromGlyph.prototype.digest = function () {
        return {
            name: "RemoveMarkFromGlyph",
            glyph: core_1.objectDigest(this.glyph),
            mark: core_1.objectDigest(this.mark),
        };
    };
    return RemoveMarkFromGlyph;
}(core_1.Action));
exports.RemoveMarkFromGlyph = RemoveMarkFromGlyph;
/**
 * Dispatches when user binds table coulmns to attributes
 */
var MapDataToMarkAttribute = /** @class */ (function (_super) {
    __extends(MapDataToMarkAttribute, _super);
    /**
     * @param glyph the glyph object where marks is
     * @param mark mark object for which the attribute is being changed
     * @param attribute name of the attribute that data is associated with
     * @param attributeType attribute data type
     * @param expression expression to fetch data from table. Usually contains name of column and aggregation function
     * @param valueType type of data in the column
     * @param valueMetadata additional data about column
     * @param hints contains configuration of data mapping to attribute
     */
    function MapDataToMarkAttribute(glyph, mark, attribute, attributeType, expression, valueType, valueMetadata, hints, expressionTable) {
        var _this = _super.call(this) || this;
        _this.glyph = glyph;
        _this.mark = mark;
        _this.attribute = attribute;
        _this.attributeType = attributeType;
        _this.expression = expression;
        _this.valueType = valueType;
        _this.valueMetadata = valueMetadata;
        _this.hints = hints;
        _this.expressionTable = expressionTable;
        return _this;
    }
    MapDataToMarkAttribute.prototype.digest = function () {
        return {
            name: "MapDataToMarkAttribute",
            glyph: core_1.objectDigest(this.glyph),
            mark: core_1.objectDigest(this.mark),
            attribute: this.attribute,
            attributeType: this.attributeType,
            expression: this.expression,
            valueType: this.valueType,
            hints: this.hints,
        };
    };
    return MapDataToMarkAttribute;
}(core_1.Action));
exports.MapDataToMarkAttribute = MapDataToMarkAttribute;
var MarkAction = /** @class */ (function (_super) {
    __extends(MarkAction, _super);
    function MarkAction() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return MarkAction;
}(core_1.Action));
exports.MarkAction = MarkAction;
var SetMarkAttribute = /** @class */ (function (_super) {
    __extends(SetMarkAttribute, _super);
    function SetMarkAttribute(glyph, mark, attribute, mapping) {
        var _this = _super.call(this) || this;
        _this.glyph = glyph;
        _this.mark = mark;
        _this.attribute = attribute;
        _this.mapping = mapping;
        return _this;
    }
    SetMarkAttribute.prototype.digest = function () {
        return {
            name: "SetMarkAttribute",
            glyph: core_1.objectDigest(this.glyph),
            mark: core_1.objectDigest(this.mark),
            attribute: this.attribute,
            mapping: this.mapping,
        };
    };
    return SetMarkAttribute;
}(MarkAction));
exports.SetMarkAttribute = SetMarkAttribute;
var UnmapMarkAttribute = /** @class */ (function (_super) {
    __extends(UnmapMarkAttribute, _super);
    function UnmapMarkAttribute(glyph, mark, attribute) {
        var _this = _super.call(this) || this;
        _this.glyph = glyph;
        _this.mark = mark;
        _this.attribute = attribute;
        return _this;
    }
    UnmapMarkAttribute.prototype.digest = function () {
        return {
            name: "UnmapMarkAttribute",
            glyph: core_1.objectDigest(this.glyph),
            mark: core_1.objectDigest(this.mark),
            attribute: this.attribute,
        };
    };
    return UnmapMarkAttribute;
}(MarkAction));
exports.UnmapMarkAttribute = UnmapMarkAttribute;
var UpdateMarkAttribute = /** @class */ (function (_super) {
    __extends(UpdateMarkAttribute, _super);
    function UpdateMarkAttribute(glyph, mark, updates) {
        var _this = _super.call(this) || this;
        _this.glyph = glyph;
        _this.mark = mark;
        _this.updates = updates;
        return _this;
    }
    UpdateMarkAttribute.prototype.digest = function () {
        return {
            name: "UpdateMarkAttribute",
            glyph: core_1.objectDigest(this.glyph),
            mark: core_1.objectDigest(this.mark),
            updates: this.updates,
        };
    };
    return UpdateMarkAttribute;
}(MarkAction));
exports.UpdateMarkAttribute = UpdateMarkAttribute;
var SnapMarks = /** @class */ (function (_super) {
    __extends(SnapMarks, _super);
    function SnapMarks(glyph, mark, attribute, targetMark, targetAttribute) {
        var _this = _super.call(this) || this;
        _this.glyph = glyph;
        _this.mark = mark;
        _this.attribute = attribute;
        _this.targetMark = targetMark;
        _this.targetAttribute = targetAttribute;
        return _this;
    }
    SnapMarks.prototype.digest = function () {
        return {
            name: "SnapMarks",
            glyph: core_1.objectDigest(this.glyph),
            mark: core_1.objectDigest(this.mark),
            attribute: this.attribute,
            targetMark: core_1.objectDigest(this.targetMark),
            targetAttribute: this.targetAttribute,
        };
    };
    return SnapMarks;
}(MarkAction));
exports.SnapMarks = SnapMarks;
var MarkActionGroup = /** @class */ (function (_super) {
    __extends(MarkActionGroup, _super);
    function MarkActionGroup(actions) {
        if (actions === void 0) { actions = []; }
        var _this = _super.call(this) || this;
        _this.actions = actions;
        return _this;
    }
    MarkActionGroup.prototype.add = function (action) {
        this.actions.push(action);
    };
    MarkActionGroup.prototype.digest = function () {
        return {
            name: "MarkActionGroup",
            actions: this.actions.map(function (x) { return x.digest(); }),
        };
    };
    return MarkActionGroup;
}(MarkAction));
exports.MarkActionGroup = MarkActionGroup;
var SetGlyphAttribute = /** @class */ (function (_super) {
    __extends(SetGlyphAttribute, _super);
    function SetGlyphAttribute(glyph, attribute, mapping) {
        var _this = _super.call(this) || this;
        _this.glyph = glyph;
        _this.attribute = attribute;
        _this.mapping = mapping;
        return _this;
    }
    SetGlyphAttribute.prototype.digest = function () {
        return {
            name: "SetGlyphAttribute",
            glyph: core_1.objectDigest(this.glyph),
            attribute: this.attribute,
            mapping: this.mapping,
        };
    };
    return SetGlyphAttribute;
}(core_1.Action));
exports.SetGlyphAttribute = SetGlyphAttribute;
var UpdateGlyphAttribute = /** @class */ (function (_super) {
    __extends(UpdateGlyphAttribute, _super);
    function UpdateGlyphAttribute(glyph, updates) {
        var _this = _super.call(this) || this;
        _this.glyph = glyph;
        _this.updates = updates;
        return _this;
    }
    UpdateGlyphAttribute.prototype.digest = function () {
        return {
            name: "UpdateGlyphAttribute",
            glyph: core_1.objectDigest(this.glyph),
            updates: this.updates,
        };
    };
    return UpdateGlyphAttribute;
}(core_1.Action));
exports.UpdateGlyphAttribute = UpdateGlyphAttribute;
var AddChartElement = /** @class */ (function (_super) {
    __extends(AddChartElement, _super);
    function AddChartElement(classID, mappings, properties) {
        if (properties === void 0) { properties = {}; }
        var _this = _super.call(this) || this;
        _this.classID = classID;
        _this.mappings = mappings;
        _this.properties = properties;
        return _this;
    }
    AddChartElement.prototype.digest = function () {
        return {
            name: "AddChartElement",
            classID: this.classID,
            mappings: this.mappings,
            attribute: this.properties,
        };
    };
    return AddChartElement;
}(core_1.Action));
exports.AddChartElement = AddChartElement;
var DeleteChartElement = /** @class */ (function (_super) {
    __extends(DeleteChartElement, _super);
    function DeleteChartElement(chartElement) {
        var _this = _super.call(this) || this;
        _this.chartElement = chartElement;
        return _this;
    }
    DeleteChartElement.prototype.digest = function () {
        return {
            name: "DeleteChartElement",
            chartElement: core_1.objectDigest(this.chartElement),
        };
    };
    return DeleteChartElement;
}(core_1.Action));
exports.DeleteChartElement = DeleteChartElement;
var SetChartElementMapping = /** @class */ (function (_super) {
    __extends(SetChartElementMapping, _super);
    function SetChartElementMapping(chartElement, attribute, mapping) {
        var _this = _super.call(this) || this;
        _this.chartElement = chartElement;
        _this.attribute = attribute;
        _this.mapping = mapping;
        return _this;
    }
    SetChartElementMapping.prototype.digest = function () {
        return {
            name: "SetChartElementMapping",
            chartElement: core_1.objectDigest(this.chartElement),
            attribute: this.attribute,
            mapping: this.mapping,
        };
    };
    return SetChartElementMapping;
}(core_1.Action));
exports.SetChartElementMapping = SetChartElementMapping;
var MapDataToChartElementAttribute = /** @class */ (function (_super) {
    __extends(MapDataToChartElementAttribute, _super);
    function MapDataToChartElementAttribute(chartElement, attribute, attributeType, table, expression, valueType, valueMetadata, hints) {
        var _this = _super.call(this) || this;
        _this.chartElement = chartElement;
        _this.attribute = attribute;
        _this.attributeType = attributeType;
        _this.table = table;
        _this.expression = expression;
        _this.valueType = valueType;
        _this.valueMetadata = valueMetadata;
        _this.hints = hints;
        return _this;
    }
    MapDataToChartElementAttribute.prototype.digest = function () {
        return {
            name: "MapChartElementkAttribute",
            chartElement: core_1.objectDigest(this.chartElement),
            attribute: this.attribute,
            attributeType: this.attributeType,
            expression: this.expression,
            valueType: this.valueType,
            hints: this.hints,
        };
    };
    return MapDataToChartElementAttribute;
}(core_1.Action));
exports.MapDataToChartElementAttribute = MapDataToChartElementAttribute;
var SetPlotSegmentFilter = /** @class */ (function (_super) {
    __extends(SetPlotSegmentFilter, _super);
    function SetPlotSegmentFilter(plotSegment, filter) {
        var _this = _super.call(this) || this;
        _this.plotSegment = plotSegment;
        _this.filter = filter;
        return _this;
    }
    SetPlotSegmentFilter.prototype.digest = function () {
        return {
            name: "SetPlotSegmentFilter",
            plotSegment: core_1.objectDigest(this.plotSegment),
            filter: this.filter,
        };
    };
    return SetPlotSegmentFilter;
}(core_1.Action));
exports.SetPlotSegmentFilter = SetPlotSegmentFilter;
var SetPlotSegmentGroupBy = /** @class */ (function (_super) {
    __extends(SetPlotSegmentGroupBy, _super);
    function SetPlotSegmentGroupBy(plotSegment, groupBy) {
        var _this = _super.call(this) || this;
        _this.plotSegment = plotSegment;
        _this.groupBy = groupBy;
        return _this;
    }
    SetPlotSegmentGroupBy.prototype.digest = function () {
        return {
            name: "SetPlotSegmentGroupBy",
            plotSegment: core_1.objectDigest(this.plotSegment),
            groupBy: this.groupBy,
        };
    };
    return SetPlotSegmentGroupBy;
}(core_1.Action));
exports.SetPlotSegmentGroupBy = SetPlotSegmentGroupBy;
var SetScaleAttribute = /** @class */ (function (_super) {
    __extends(SetScaleAttribute, _super);
    function SetScaleAttribute(scale, attribute, mapping) {
        var _this = _super.call(this) || this;
        _this.scale = scale;
        _this.attribute = attribute;
        _this.mapping = mapping;
        return _this;
    }
    SetScaleAttribute.prototype.digest = function () {
        return {
            name: "SetScaleAttribute",
            scale: core_1.objectDigest(this.scale),
            attribute: this.attribute,
            mapping: this.mapping,
        };
    };
    return SetScaleAttribute;
}(core_1.Action));
exports.SetScaleAttribute = SetScaleAttribute;
var ToggleLegendForScale = /** @class */ (function (_super) {
    __extends(ToggleLegendForScale, _super);
    function ToggleLegendForScale(scale, mapping, plotSegment) {
        var _this = _super.call(this) || this;
        _this.scale = scale;
        _this.mapping = mapping;
        _this.plotSegment = plotSegment;
        return _this;
    }
    ToggleLegendForScale.prototype.digest = function () {
        return {
            name: "ToggleLegendForScale",
            scale: this.scale,
            mapping: this.mapping.expression,
        };
    };
    return ToggleLegendForScale;
}(core_1.Action));
exports.ToggleLegendForScale = ToggleLegendForScale;
var UpdateChartElementAttribute = /** @class */ (function (_super) {
    __extends(UpdateChartElementAttribute, _super);
    function UpdateChartElementAttribute(chartElement, updates) {
        var _this = _super.call(this) || this;
        _this.chartElement = chartElement;
        _this.updates = updates;
        return _this;
    }
    UpdateChartElementAttribute.prototype.digest = function () {
        return {
            name: "UpdateChartElementAttribute",
            chartElement: core_1.objectDigest(this.chartElement),
            updates: this.updates,
        };
    };
    return UpdateChartElementAttribute;
}(core_1.Action));
exports.UpdateChartElementAttribute = UpdateChartElementAttribute;
var SnapChartElements = /** @class */ (function (_super) {
    __extends(SnapChartElements, _super);
    function SnapChartElements(element, attribute, targetElement, targetAttribute) {
        var _this = _super.call(this) || this;
        _this.element = element;
        _this.attribute = attribute;
        _this.targetElement = targetElement;
        _this.targetAttribute = targetAttribute;
        return _this;
    }
    SnapChartElements.prototype.digest = function () {
        return {
            name: "SnapChartElements",
            element: core_1.objectDigest(this.element),
            attribute: this.attribute,
            targetElement: core_1.objectDigest(this.targetElement),
            targetAttribute: this.targetAttribute,
        };
    };
    return SnapChartElements;
}(core_1.Action));
exports.SnapChartElements = SnapChartElements;
var BindDataToAxis = /** @class */ (function (_super) {
    __extends(BindDataToAxis, _super);
    function BindDataToAxis(object, property, appendToProperty, dataExpression, defineCategories, type, numericalMode) {
        var _this = _super.call(this) || this;
        _this.object = object;
        _this.property = property;
        _this.appendToProperty = appendToProperty;
        _this.dataExpression = dataExpression;
        _this.defineCategories = defineCategories;
        _this.type = type;
        _this.numericalMode = numericalMode;
        return _this;
    }
    BindDataToAxis.prototype.digest = function () {
        return {
            name: "BindDataToAxis",
            object: core_1.objectDigest(this.object),
            property: this.property,
            appendToProperty: this.appendToProperty,
            dataExpression: {
                table: this.dataExpression.table.name,
                expression: this.dataExpression.expression,
                valueType: this.dataExpression.valueType,
                kind: this.dataExpression.metadata.kind,
                allowSelectValue: this.dataExpression.allowSelectValue,
            },
            type: this.type,
            numericalMode: this.numericalMode,
        };
    };
    return BindDataToAxis;
}(core_1.Action));
exports.BindDataToAxis = BindDataToAxis;
var AddLinks = /** @class */ (function (_super) {
    __extends(AddLinks, _super);
    function AddLinks(links) {
        var _this = _super.call(this) || this;
        _this.links = links;
        return _this;
    }
    AddLinks.prototype.digest = function () {
        return {
            name: "AddLinks",
            links: this.links,
        };
    };
    return AddLinks;
}(core_1.Action));
exports.AddLinks = AddLinks;
var UpdateChartAttribute = /** @class */ (function (_super) {
    __extends(UpdateChartAttribute, _super);
    function UpdateChartAttribute(chart, updates) {
        var _this = _super.call(this) || this;
        _this.chart = chart;
        _this.updates = updates;
        return _this;
    }
    UpdateChartAttribute.prototype.digest = function () {
        return {
            name: "UpdateChartAttribute",
            updates: this.updates,
        };
    };
    return UpdateChartAttribute;
}(core_1.Action));
exports.UpdateChartAttribute = UpdateChartAttribute;
var SetChartSize = /** @class */ (function (_super) {
    __extends(SetChartSize, _super);
    function SetChartSize(width, height) {
        var _this = _super.call(this) || this;
        _this.width = width;
        _this.height = height;
        return _this;
    }
    SetChartSize.prototype.digest = function () {
        return {
            name: "SetChartSize",
            width: this.width,
            height: this.height,
        };
    };
    return SetChartSize;
}(core_1.Action));
exports.SetChartSize = SetChartSize;
var SetChartAttribute = /** @class */ (function (_super) {
    __extends(SetChartAttribute, _super);
    function SetChartAttribute(attribute, mapping) {
        var _this = _super.call(this) || this;
        _this.attribute = attribute;
        _this.mapping = mapping;
        return _this;
    }
    SetChartAttribute.prototype.digest = function () {
        return {
            name: "SetChartAttribute",
            attribute: this.attribute,
            mapping: this.mapping,
        };
    };
    return SetChartAttribute;
}(core_1.Action));
exports.SetChartAttribute = SetChartAttribute;
var SetObjectProperty = /** @class */ (function (_super) {
    __extends(SetObjectProperty, _super);
    function SetObjectProperty(object, property, field, value, noUpdateState, noComputeLayout) {
        if (noUpdateState === void 0) { noUpdateState = false; }
        if (noComputeLayout === void 0) { noComputeLayout = false; }
        var _this = _super.call(this) || this;
        _this.object = object;
        _this.property = property;
        _this.field = field;
        _this.value = value;
        _this.noUpdateState = noUpdateState;
        _this.noComputeLayout = noComputeLayout;
        return _this;
    }
    SetObjectProperty.prototype.digest = function () {
        return {
            name: "SetObjectProperty",
            object: core_1.objectDigest(this.object),
            property: this.property,
            field: this.field,
            value: this.value,
            noUpdateState: this.noUpdateState,
            noComputeLayout: this.noComputeLayout,
        };
    };
    return SetObjectProperty;
}(core_1.Action));
exports.SetObjectProperty = SetObjectProperty;
var DeleteObjectProperty = /** @class */ (function (_super) {
    __extends(DeleteObjectProperty, _super);
    function DeleteObjectProperty(object, property, field, noUpdateState, noComputeLayout) {
        if (noUpdateState === void 0) { noUpdateState = false; }
        if (noComputeLayout === void 0) { noComputeLayout = false; }
        var _this = _super.call(this) || this;
        _this.object = object;
        _this.property = property;
        _this.field = field;
        _this.noUpdateState = noUpdateState;
        _this.noComputeLayout = noComputeLayout;
        return _this;
    }
    DeleteObjectProperty.prototype.digest = function () {
        return {
            name: "DeleteObjectProperty",
            object: core_1.objectDigest(this.object),
            property: this.property,
            field: this.field,
            noUpdateState: this.noUpdateState,
            noComputeLayout: this.noComputeLayout,
        };
    };
    return DeleteObjectProperty;
}(core_1.Action));
exports.DeleteObjectProperty = DeleteObjectProperty;
var SetObjectMappingScale = /** @class */ (function (_super) {
    __extends(SetObjectMappingScale, _super);
    function SetObjectMappingScale(object, property, scaleId) {
        var _this = _super.call(this) || this;
        _this.object = object;
        _this.property = property;
        _this.scaleId = scaleId;
        return _this;
    }
    SetObjectMappingScale.prototype.digest = function () {
        return {
            name: "SetObjectProperty",
            object: core_1.objectDigest(this.object),
            property: this.property,
            scaleId: this.scaleId,
        };
    };
    return SetObjectMappingScale;
}(core_1.Action));
exports.SetObjectMappingScale = SetObjectMappingScale;
var ExtendPlotSegment = /** @class */ (function (_super) {
    __extends(ExtendPlotSegment, _super);
    function ExtendPlotSegment(plotSegment, extension) {
        var _this = _super.call(this) || this;
        _this.plotSegment = plotSegment;
        _this.extension = extension;
        return _this;
    }
    ExtendPlotSegment.prototype.digest = function () {
        return {
            name: "ExtendPlotSegment",
            plotSegment: core_1.objectDigest(this.plotSegment),
            extension: this.extension,
        };
    };
    return ExtendPlotSegment;
}(core_1.Action));
exports.ExtendPlotSegment = ExtendPlotSegment;
var ReorderChartElement = /** @class */ (function (_super) {
    __extends(ReorderChartElement, _super);
    function ReorderChartElement(fromIndex, toIndex) {
        var _this = _super.call(this) || this;
        _this.fromIndex = fromIndex;
        _this.toIndex = toIndex;
        return _this;
    }
    ReorderChartElement.prototype.digest = function () {
        return {
            name: "ReorderChartElement",
            fromIndex: this.fromIndex,
            toIndex: this.toIndex,
        };
    };
    return ReorderChartElement;
}(core_1.Action));
exports.ReorderChartElement = ReorderChartElement;
var ReorderGlyphMark = /** @class */ (function (_super) {
    __extends(ReorderGlyphMark, _super);
    function ReorderGlyphMark(glyph, fromIndex, toIndex) {
        var _this = _super.call(this) || this;
        _this.glyph = glyph;
        _this.fromIndex = fromIndex;
        _this.toIndex = toIndex;
        return _this;
    }
    ReorderGlyphMark.prototype.digest = function () {
        return {
            name: "ReorderGlyphMark",
            glyph: core_1.objectDigest(this.glyph),
            fromIndex: this.fromIndex,
            toIndex: this.toIndex,
        };
    };
    return ReorderGlyphMark;
}(core_1.Action));
exports.ReorderGlyphMark = ReorderGlyphMark;
var SelectGlyph = /** @class */ (function (_super) {
    __extends(SelectGlyph, _super);
    function SelectGlyph(plotSegment, glyph, glyphIndex) {
        if (glyphIndex === void 0) { glyphIndex = null; }
        var _this = _super.call(this) || this;
        _this.plotSegment = plotSegment;
        _this.glyph = glyph;
        _this.glyphIndex = glyphIndex;
        return _this;
    }
    SelectGlyph.prototype.digest = function () {
        return {
            name: "SelectGlyph",
            plotSegment: core_1.objectDigest(this.plotSegment),
            glyph: core_1.objectDigest(this.glyph),
            glyphIndex: this.glyphIndex,
        };
    };
    return SelectGlyph;
}(core_1.Action));
exports.SelectGlyph = SelectGlyph;
var SelectChartElement = /** @class */ (function (_super) {
    __extends(SelectChartElement, _super);
    function SelectChartElement(chartElement, glyphIndex) {
        if (glyphIndex === void 0) { glyphIndex = null; }
        var _this = _super.call(this) || this;
        _this.chartElement = chartElement;
        _this.glyphIndex = glyphIndex;
        return _this;
    }
    SelectChartElement.prototype.digest = function () {
        return {
            name: "SelectChartElement",
            glyph: core_1.objectDigest(this.chartElement),
            glyphIndex: this.glyphIndex,
        };
    };
    return SelectChartElement;
}(core_1.Action));
exports.SelectChartElement = SelectChartElement;
var FocusToMarkAttribute = /** @class */ (function (_super) {
    __extends(FocusToMarkAttribute, _super);
    function FocusToMarkAttribute(attributeName) {
        var _this = _super.call(this) || this;
        _this.attributeName = attributeName;
        return _this;
    }
    FocusToMarkAttribute.prototype.digest = function () {
        return {
            name: "FocusToMarkAttribute",
            attributeName: this.attributeName,
        };
    };
    return FocusToMarkAttribute;
}(core_1.Action));
exports.FocusToMarkAttribute = FocusToMarkAttribute;
var SetCurrentMappingAttribute = /** @class */ (function (_super) {
    __extends(SetCurrentMappingAttribute, _super);
    function SetCurrentMappingAttribute(attributeName) {
        var _this = _super.call(this) || this;
        _this.attributeName = attributeName;
        return _this;
    }
    SetCurrentMappingAttribute.prototype.digest = function () {
        return {
            name: "SetCurrentMappingAttribute",
            attributeName: this.attributeName,
        };
    };
    return SetCurrentMappingAttribute;
}(core_1.Action));
exports.SetCurrentMappingAttribute = SetCurrentMappingAttribute;
var SetCurrentTool = /** @class */ (function (_super) {
    __extends(SetCurrentTool, _super);
    function SetCurrentTool(tool, options) {
        if (options === void 0) { options = null; }
        var _this = _super.call(this) || this;
        _this.tool = tool;
        _this.options = options;
        return _this;
    }
    SetCurrentTool.prototype.digest = function () {
        return {
            name: "SetCurrentTool",
            tool: this.tool,
            options: this.options,
        };
    };
    return SetCurrentTool;
}(core_1.Action));
exports.SetCurrentTool = SetCurrentTool;
var AddMessage = /** @class */ (function (_super) {
    __extends(AddMessage, _super);
    function AddMessage(type, options) {
        if (options === void 0) { options = {}; }
        var _this = _super.call(this) || this;
        _this.type = type;
        _this.options = options;
        return _this;
    }
    AddMessage.prototype.digest = function () {
        return { name: "AddMessage", type: this.type, options: this.options };
    };
    return AddMessage;
}(core_1.Action));
exports.AddMessage = AddMessage;
var RemoveMessage = /** @class */ (function (_super) {
    __extends(RemoveMessage, _super);
    function RemoveMessage(type) {
        var _this = _super.call(this) || this;
        _this.type = type;
        return _this;
    }
    RemoveMessage.prototype.digest = function () {
        return { name: "RemoveMessage", type: this.type };
    };
    return RemoveMessage;
}(core_1.Action));
exports.RemoveMessage = RemoveMessage;
var ClearMessages = /** @class */ (function (_super) {
    __extends(ClearMessages, _super);
    function ClearMessages() {
        return _super.call(this) || this;
    }
    ClearMessages.prototype.digest = function () {
        return { name: "ClearMessages" };
    };
    return ClearMessages;
}(core_1.Action));
exports.ClearMessages = ClearMessages;
var OpenNestedEditor = /** @class */ (function (_super) {
    __extends(OpenNestedEditor, _super);
    function OpenNestedEditor(object, property, options) {
        var _this = _super.call(this) || this;
        _this.object = object;
        _this.property = property;
        _this.options = options;
        return _this;
    }
    OpenNestedEditor.prototype.digest = function () {
        return { name: "OpenNestedEditor" };
    };
    return OpenNestedEditor;
}(core_1.Action));
exports.OpenNestedEditor = OpenNestedEditor;
var SearchUpdated = /** @class */ (function (_super) {
    __extends(SearchUpdated, _super);
    function SearchUpdated(searchString) {
        var _this = _super.call(this) || this;
        _this.searchString = searchString;
        return _this;
    }
    SearchUpdated.prototype.digest = function () {
        return { name: "SearchUpdated" };
    };
    return SearchUpdated;
}(core_1.Action));
exports.SearchUpdated = SearchUpdated;
var ExpandOrCollapsePanelsUpdated = /** @class */ (function (_super) {
    __extends(ExpandOrCollapsePanelsUpdated, _super);
    function ExpandOrCollapsePanelsUpdated(type) {
        var _this = _super.call(this) || this;
        _this.type = type;
        return _this;
    }
    ExpandOrCollapsePanelsUpdated.prototype.digest = function () {
        return { name: "ExpandOrCollapsePanelsUpdated" };
    };
    return ExpandOrCollapsePanelsUpdated;
}(core_1.Action));
exports.ExpandOrCollapsePanelsUpdated = ExpandOrCollapsePanelsUpdated;
//# sourceMappingURL=actions.js.map