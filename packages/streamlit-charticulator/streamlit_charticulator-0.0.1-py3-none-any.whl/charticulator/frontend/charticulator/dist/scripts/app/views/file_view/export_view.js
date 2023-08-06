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
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __values = (this && this.__values) || function(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
var __read = (this && this.__read) || function (o, n) {
    var m = typeof Symbol === "function" && o[Symbol.iterator];
    if (!m) return o;
    var i = m.call(o), r, ar = [], e;
    try {
        while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
    }
    catch (error) { e = { error: error }; }
    finally {
        try {
            if (r && !r.done && (m = i["return"])) m.call(i);
        }
        finally { if (e) throw e.error; }
    }
    return ar;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ExportTemplateView = exports.FileViewExport = exports.ExportHTMLView = exports.ExportImageView = exports.InputGroup = void 0;
var react_1 = require("@fluentui/react");
var React = require("react");
var _1 = require(".");
var core_1 = require("../../../core");
var examples_1 = require("../../../core/dataset/examples");
var prototypes_1 = require("../../../core/prototypes");
var strings_1 = require("../../../strings");
var actions_1 = require("../../actions");
var components_1 = require("../../components");
var R = require("../../resources");
var utils_1 = require("../../utils");
var controls_1 = require("../panels/widgets/controls");
var noop_1 = require("../../utils/noop");
var InputGroup = /** @class */ (function (_super) {
    __extends(InputGroup, _super);
    function InputGroup() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    InputGroup.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", { className: "form-group" },
            React.createElement("input", { ref: function (e) { return (_this.ref = e); }, type: "text", required: true, value: this.props.value || "", onChange: function () {
                    _this.props.onChange(_this.ref.value);
                } }),
            React.createElement("label", null, this.props.label),
            React.createElement("i", { className: "bar" })));
    };
    return InputGroup;
}(React.Component));
exports.InputGroup = InputGroup;
var ExportImageView = /** @class */ (function (_super) {
    __extends(ExportImageView, _super);
    function ExportImageView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { dpi: "144" };
        return _this;
    }
    ExportImageView.prototype.getScaler = function () {
        var dpi = +this.state.dpi;
        if (dpi < 1 || dpi != dpi) {
            dpi = 144;
        }
        dpi = Math.max(Math.min(dpi, 1200), 36);
        return dpi / 72;
    };
    ExportImageView.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", { className: "el-horizontal-layout-item is-fix-width" },
            React.createElement(_1.CurrentChartView, { store: this.props.store }),
            React.createElement(InputGroup, { label: strings_1.strings.fileExport.imageDPI, value: this.state.dpi, onChange: function (newValue) {
                    _this.setState({
                        dpi: newValue,
                    });
                } }),
            React.createElement("div", { className: "buttons" },
                React.createElement(react_1.DefaultButton, { text: strings_1.strings.fileExport.typePNG, iconProps: {
                        iconName: "Export",
                    }, styles: core_1.primaryButtonStyles, onClick: function () {
                        _this.props.store.dispatcher.dispatch(new actions_1.Actions.Export("png", { scale: _this.getScaler() }));
                    } }),
                " ",
                React.createElement(react_1.DefaultButton, { text: strings_1.strings.fileExport.typeJPEG, iconProps: {
                        iconName: "Export",
                    }, styles: core_1.primaryButtonStyles, onClick: function () {
                        _this.props.store.dispatcher.dispatch(new actions_1.Actions.Export("jpeg", { scale: _this.getScaler() }));
                    } }),
                " ",
                React.createElement(react_1.DefaultButton, { text: strings_1.strings.fileExport.typeSVG, iconProps: {
                        iconName: "Export",
                    }, styles: core_1.primaryButtonStyles, onClick: function () {
                        _this.props.store.dispatcher.dispatch(new actions_1.Actions.Export("svg"));
                    } }))));
    };
    return ExportImageView;
}(React.Component));
exports.ExportImageView = ExportImageView;
var ExportHTMLView = /** @class */ (function (_super) {
    __extends(ExportHTMLView, _super);
    function ExportHTMLView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ExportHTMLView.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", { className: "el-horizontal-layout-item is-fix-width" },
            React.createElement(_1.CurrentChartView, { store: this.props.store }),
            React.createElement("div", { className: "buttons" },
                React.createElement(react_1.DefaultButton, { text: strings_1.strings.fileExport.typeHTML, iconProps: {
                        iconName: "Export",
                    }, styles: core_1.primaryButtonStyles, onClick: function () {
                        _this.props.store.dispatcher.dispatch(new actions_1.Actions.Export("html"));
                    } }))));
    };
    return ExportHTMLView;
}(React.Component));
exports.ExportHTMLView = ExportHTMLView;
var FileViewExport = /** @class */ (function (_super) {
    __extends(FileViewExport, _super);
    function FileViewExport() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            exportMode: "image",
        };
        return _this;
    }
    FileViewExport.prototype.renderExportView = function (mode) {
        if (mode == "image") {
            return React.createElement(ExportImageView, { store: this.props.store });
        }
        if (mode == "html") {
            return React.createElement(ExportHTMLView, { store: this.props.store });
        }
    };
    FileViewExport.prototype.renderExportTemplate = function () {
        return (React.createElement("div", { className: "el-horizontal-layout-item is-fix-width" },
            React.createElement(_1.CurrentChartView, { store: this.props.store }),
            React.createElement(ExportTemplateView, { store: this.props.store, exportKind: this.state.exportMode })));
    };
    FileViewExport.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", { className: "charticulator__file-view-content" },
            React.createElement("h1", null, strings_1.strings.mainTabs.export),
            React.createElement("div", { className: "el-horizontal-layout" },
                React.createElement("div", { className: "el-horizontal-layout-item" },
                    React.createElement("div", { className: "charticulator__list-view" },
                        React.createElement("div", { tabIndex: 0, className: utils_1.classNames("el-item", [
                                "is-active",
                                this.state.exportMode == "image",
                            ]), onClick: function () { return _this.setState({ exportMode: "image" }); }, onKeyPress: function (e) {
                                if (e.key === "Enter") {
                                    _this.setState({ exportMode: "image" });
                                }
                            } },
                            React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon("toolbar/export") }),
                            React.createElement("span", { className: "el-text" }, strings_1.strings.fileExport.asImage)),
                        React.createElement("div", { tabIndex: 0, className: utils_1.classNames("el-item", [
                                "is-active",
                                this.state.exportMode == "html",
                            ]), onClick: function () { return _this.setState({ exportMode: "html" }); }, onKeyPress: function (e) {
                                if (e.key === "Enter") {
                                    _this.setState({ exportMode: "html" });
                                }
                            } },
                            React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon("toolbar/export") }),
                            React.createElement("span", { className: "el-text" }, strings_1.strings.fileExport.asHTML)),
                        this.props.store.listExportTemplateTargets().map(function (name) { return (React.createElement("div", { tabIndex: 0, key: name, className: utils_1.classNames("el-item", [
                                "is-active",
                                _this.state.exportMode == name,
                            ]), onClick: function () { return _this.setState({ exportMode: name }); }, onKeyPress: function (e) {
                                if (e.key === "Enter") {
                                    _this.setState({ exportMode: name });
                                }
                            } },
                            React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon("toolbar/export") }),
                            React.createElement("span", { className: "el-text" }, name))); }))),
                React.createElement(components_1.TelemetryContext.Consumer, null, function (telemetryRecorder) {
                    return (React.createElement(components_1.ErrorBoundary, { maxWidth: 300, telemetryRecorder: telemetryRecorder }, _this.state.exportMode == "image" ||
                        _this.state.exportMode == "html"
                        ? _this.renderExportView(_this.state.exportMode)
                        : _this.renderExportTemplate()));
                }))));
    };
    return FileViewExport;
}(React.Component));
exports.FileViewExport = FileViewExport;
var ExportTemplateView = /** @class */ (function (_super) {
    __extends(ExportTemplateView, _super);
    function ExportTemplateView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getDefaultState(_this.props.exportKind);
        return _this;
    }
    ExportTemplateView.prototype.getDefaultState = function (kind) {
        var e_1, _a;
        this.props.store.dataset.tables.forEach(function (t) {
            return examples_1.ensureColumnsHaveExamples(t);
        });
        var template = core_1.deepClone(this.props.store.buildChartTemplate());
        var target = this.props.store.createExportTemplateTarget(kind, template);
        var targetProperties = {};
        try {
            for (var _b = __values(target.getProperties()), _c = _b.next(); !_c.done; _c = _b.next()) {
                var property = _c.value;
                targetProperties[property.name] =
                    this.props.store.getPropertyExportName(property.name) ||
                        property.default;
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return {
            template: template,
            target: target,
            targetProperties: targetProperties,
        };
    };
    ExportTemplateView.prototype.componentWillReceiveProps = function (newProps) {
        this.setState(this.getDefaultState(newProps.exportKind));
    };
    /** Renders input fields for extension properties */
    ExportTemplateView.prototype.renderInput = function (label, type, value, defaultValue, onChange) {
        var ref;
        switch (type) {
            case "string":
                return (React.createElement("div", { className: "form-group" },
                    React.createElement("input", { ref: function (e) { return (ref = e); }, type: "text", required: true, value: value || "", onChange: function () {
                            onChange(ref.value);
                        } }),
                    React.createElement("label", null, label),
                    React.createElement("i", { className: "bar" })));
            case "boolean":
                // eslint-disable-next-line
                var currentValue_1 = value ? true : false;
                return (React.createElement("div", { className: "el-inference-item", onClick: function () {
                        onChange(!currentValue_1);
                    } },
                    React.createElement(components_1.SVGImageIcon, { url: currentValue_1
                            ? R.getSVGIcon("checkbox/checked")
                            : R.getSVGIcon("checkbox/empty") }),
                    React.createElement("span", { className: "el-text" }, label)));
            case "file":
                return (React.createElement("div", { className: "form-group-file" },
                    React.createElement("label", null, label),
                    React.createElement("div", { style: {
                            display: "flex",
                            flexDirection: "row",
                        } },
                        React.createElement(controls_1.InputImageProperty, { value: value, onChange: function (image) {
                                onChange(image);
                                return true;
                            } }),
                        React.createElement(controls_1.Button, { icon: "general/eraser", onClick: function () {
                                onChange(defaultValue);
                            } })),
                    React.createElement("i", { className: "bar" })));
        }
    };
    /** Renders all fields for extension properties */
    ExportTemplateView.prototype.renderTargetProperties = function () {
        var _this = this;
        return this.state.target.getProperties().map(function (property) {
            var displayName = _this.props.store.getPropertyExportName(property.name);
            var targetProperties = _this.state.targetProperties;
            return (React.createElement("div", { key: property.name }, _this.renderInput(property.displayName, property.type, displayName || targetProperties[property.name], property.default, function (value) {
                var _a;
                _this.props.store.setPropertyExportName(property.name, value);
                _this.setState({
                    targetProperties: __assign(__assign({}, targetProperties), (_a = {}, _a[property.name] = value, _a)),
                });
            })));
        });
    };
    /** Renders column names for export view */
    ExportTemplateView.prototype.renderSlots = function () {
        var _this = this;
        if (this.state.template.tables.length == 0) {
            return React.createElement("p", null, strings_1.strings.core.none);
        }
        return this.state.template.tables.map(function (table) { return (React.createElement("div", { key: table.name }, table.columns
            .filter(function (col) { return !col.metadata.isRaw; })
            .map(function (column) { return (React.createElement("div", { key: column.name },
            _this.renderInput(strings_1.strings.fileExport.slotColumnName(column.name), "string", column.displayName, null, function (value) {
                var originalColumn = _this.getOriginalColumn(table.name, column.name);
                [originalColumn, column].forEach(function (c) { return (c.displayName = value); });
                _this.setState({
                    template: _this.state.template,
                });
            }),
            _this.renderInput(strings_1.strings.fileExport.slotColumnExample(column.name), "string", column.metadata.examples, null, function (value) {
                var originalColumn = _this.getOriginalColumn(table.name, column.name);
                [originalColumn, column].forEach(function (c) { return (c.metadata.examples = value); });
                _this.setState({
                    template: _this.state.template,
                });
            }))); }))); });
    };
    ExportTemplateView.prototype.getOriginalColumn = function (tableName, columnName) {
        var dataTable = this.props.store.dataset.tables.find(function (t) { return t.name === tableName; });
        var dataColumn = dataTable.columns.find(function (c) { return c.name === columnName; });
        return dataColumn;
    };
    // eslint-disable-next-line
    ExportTemplateView.prototype.renderInferences = function () {
        var _this = this;
        var template = this.state.template;
        if (template.inference.length == 0) {
            return React.createElement("p", null, strings_1.strings.core.none);
        }
        return (template.inference
            // Only show axis and scale inferences
            .filter(function (inference) { return inference.axis || inference.scale; })
            // eslint-disable-next-line
            .map(function (inference, index) {
            var descriptionMin;
            var descriptionMax;
            var object = prototypes_1.findObjectById(_this.props.store.chart, inference.objectID);
            var temaplteObject = prototypes_1.findObjectById(template.specification, inference.objectID);
            var objectName = object.properties.name;
            if (inference.scale) {
                descriptionMin = strings_1.strings.fileExport.inferScaleMin(objectName);
                descriptionMax = strings_1.strings.fileExport.inferScaleMax(objectName);
            }
            if (inference.axis) {
                descriptionMin = strings_1.strings.fileExport.inferAxisMin(objectName, inference.axis.property.toString());
                descriptionMax = strings_1.strings.fileExport.inferAxisMax(objectName, inference.axis.property.toString());
            }
            var keyAutoDomainMin = "autoDomainMin";
            var keyAutoDomainMax = "autoDomainMax";
            var onClickAutoDomainMin = noop_1.noop;
            var onClickAutoDomainMax = noop_1.noop;
            var getAutoDomainMinPropertyValue = null;
            var getAutoDomainMaxPropertyValue = null;
            if (inference.axis) {
                if (object.properties[inference.axis.property][keyAutoDomainMax] === undefined) {
                    _this.props.store.dispatcher.dispatch(new actions_1.Actions.SetObjectProperty(object, inference.axis.property, keyAutoDomainMax, true, true, true));
                    temaplteObject.properties[keyAutoDomainMax] = true;
                    inference.autoDomainMax = true;
                }
                else {
                    inference.autoDomainMax = object.properties[inference.axis.property][keyAutoDomainMax];
                }
                onClickAutoDomainMax = function () {
                    _this.props.store.dispatcher.dispatch(new actions_1.Actions.SetObjectProperty(object, inference.axis.property, keyAutoDomainMax, !object.properties[inference.axis.property][keyAutoDomainMax], true, true));
                    _this.setState({ template: template });
                };
                getAutoDomainMaxPropertyValue = function () {
                    return object.properties[inference.axis.property][keyAutoDomainMax];
                };
            }
            if (inference.scale) {
                if (object.properties[keyAutoDomainMax] === undefined) {
                    _this.props.store.dispatcher.dispatch(new actions_1.Actions.SetObjectProperty(object, keyAutoDomainMax, null, true, true, true));
                    temaplteObject.properties[keyAutoDomainMax] = true;
                    inference.autoDomainMax = true;
                }
                else {
                    inference.autoDomainMax = temaplteObject.properties[keyAutoDomainMax];
                }
                onClickAutoDomainMax = function () {
                    _this.props.store.dispatcher.dispatch(new actions_1.Actions.SetObjectProperty(object, keyAutoDomainMax, null, !object.properties[keyAutoDomainMax], true, true));
                    _this.setState({ template: template });
                };
                getAutoDomainMaxPropertyValue = function () {
                    return object.properties[keyAutoDomainMax];
                };
            }
            if (inference.axis) {
                if (object.properties[inference.axis.property][keyAutoDomainMin] === undefined) {
                    _this.props.store.dispatcher.dispatch(new actions_1.Actions.SetObjectProperty(object, inference.axis.property, keyAutoDomainMin, true, true, true));
                    temaplteObject.properties[keyAutoDomainMin] = true;
                    inference.autoDomainMin = true;
                }
                else {
                    inference.autoDomainMin = object.properties[inference.axis.property][keyAutoDomainMin];
                }
                onClickAutoDomainMin = function () {
                    _this.props.store.dispatcher.dispatch(new actions_1.Actions.SetObjectProperty(object, inference.axis.property, keyAutoDomainMin, !object.properties[inference.axis.property][keyAutoDomainMin], true, true));
                    _this.setState({ template: template });
                };
                getAutoDomainMinPropertyValue = function () {
                    return object.properties[inference.axis.property][keyAutoDomainMin];
                };
            }
            if (inference.scale) {
                if (object.properties[keyAutoDomainMin] === undefined) {
                    _this.props.store.dispatcher.dispatch(new actions_1.Actions.SetObjectProperty(object, keyAutoDomainMin, null, true, true, true));
                    temaplteObject.properties[keyAutoDomainMin] = true;
                    inference.autoDomainMin = true;
                }
                else {
                    inference.autoDomainMin = object.properties[keyAutoDomainMin];
                }
                onClickAutoDomainMin = function () {
                    _this.props.store.dispatcher.dispatch(new actions_1.Actions.SetObjectProperty(object, keyAutoDomainMin, null, !object.properties[keyAutoDomainMin], true, true));
                    _this.setState({ template: template });
                };
                getAutoDomainMinPropertyValue = function () {
                    return object.properties[keyAutoDomainMin];
                };
            }
            return (React.createElement(React.Fragment, { key: index },
                React.createElement("div", { className: "el-inference-item", onClick: onClickAutoDomainMin },
                    React.createElement(components_1.SVGImageIcon, { url: getAutoDomainMinPropertyValue()
                            ? R.getSVGIcon("checkbox/checked")
                            : R.getSVGIcon("checkbox/empty") }),
                    React.createElement("span", { className: "el-text" }, descriptionMin)),
                React.createElement("div", { className: "el-inference-item", onClick: onClickAutoDomainMax },
                    React.createElement(components_1.SVGImageIcon, { url: getAutoDomainMaxPropertyValue()
                            ? R.getSVGIcon("checkbox/checked")
                            : R.getSVGIcon("checkbox/empty") }),
                    React.createElement("span", { className: "el-text" }, descriptionMax))));
        }));
    };
    /** Renders object/properties list of chart */
    ExportTemplateView.prototype.renderExposedProperties = function () {
        var e_2, _a, e_3, _b;
        var _this = this;
        var template = this.state.template;
        var result = [];
        var templateObjects = new Map();
        try {
            for (var _c = __values(this.state.template.properties), _d = _c.next(); !_d.done; _d = _c.next()) {
                var p = _d.value;
                var id = p.objectID;
                var object = prototypes_1.findObjectById(this.props.store.chart, id);
                if (object && (p.target.attribute || p.target.property)) {
                    if (object.properties.exposed == undefined) {
                        this.props.store.dispatcher.dispatch(new actions_1.Actions.SetObjectProperty(object, "exposed", null, true, true, true));
                        var templateObject = prototypes_1.findObjectById(this.state.template.specification, id);
                        templateObject.properties.exposed = true;
                    }
                    templateObjects.set(id, object);
                }
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_2) throw e_2.error; }
        }
        var _loop_1 = function (key, object) {
            if (core_1.Prototypes.isType(object.classID, "guide")) {
                return "continue";
            }
            var onClick = function () {
                _this.props.store.dispatcher.dispatch(new actions_1.Actions.SetObjectProperty(object, "exposed", null, !(object.properties.exposed === undefined
                    ? true
                    : object.properties.exposed), true, true));
                var templateObject = prototypes_1.findObjectById(_this.state.template.specification, object._id);
                templateObject.properties.exposed = !templateObject.properties.exposed;
                _this.setState({ template: template });
            };
            result.push(React.createElement("div", { "aria-checked": object.properties.exposed === undefined
                    ? "true"
                    : object.properties.exposed
                        ? "true"
                        : "false", tabIndex: 0, key: key, className: "el-inference-item", onClick: onClick, onKeyPress: function (e) {
                    if (e.key === "Enter") {
                        onClick();
                    }
                } },
                React.createElement(components_1.SVGImageIcon, { url: !(object.properties.exposed === undefined
                        ? true
                        : object.properties.exposed)
                        ? R.getSVGIcon("checkbox/empty")
                        : R.getSVGIcon("checkbox/checked") }),
                React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(core_1.Prototypes.ObjectClasses.GetMetadata(object.classID).iconPath) }),
                React.createElement("span", { className: "el-text" }, object.properties.name)));
        };
        try {
            for (var templateObjects_1 = __values(templateObjects), templateObjects_1_1 = templateObjects_1.next(); !templateObjects_1_1.done; templateObjects_1_1 = templateObjects_1.next()) {
                var _e = __read(templateObjects_1_1.value, 2), key = _e[0], object = _e[1];
                _loop_1(key, object);
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (templateObjects_1_1 && !templateObjects_1_1.done && (_b = templateObjects_1.return)) _b.call(templateObjects_1);
            }
            finally { if (e_3) throw e_3.error; }
        }
        return result;
    };
    ExportTemplateView.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", { className: "charticulator__export-template-view" },
            React.createElement("h2", null, strings_1.strings.fileExport.labelSlots),
            this.renderSlots(),
            React.createElement("h2", null, strings_1.strings.fileExport.labelAxesAndScales),
            this.renderInferences(),
            React.createElement("h2", null, strings_1.strings.fileExport.labelExposedObjects),
            this.renderExposedProperties(),
            React.createElement("h2", null, strings_1.strings.fileExport.labelProperties(this.props.exportKind)),
            this.renderTargetProperties(),
            React.createElement("div", { className: "buttons" },
                React.createElement(react_1.DefaultButton, { text: this.props.exportKind, iconProps: {
                        iconName: "Export",
                    }, styles: core_1.primaryButtonStyles, onClick: function () {
                        _this.props.store.dispatcher.dispatch(new actions_1.Actions.ExportTemplate(_this.props.exportKind, _this.state.target, _this.state.targetProperties));
                    } }))));
    };
    return ExportTemplateView;
}(React.Component));
exports.ExportTemplateView = ExportTemplateView;
//# sourceMappingURL=export_view.js.map