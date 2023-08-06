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
Object.defineProperty(exports, "__esModule", { value: true });
exports.GradientView = exports.GradientPicker = void 0;
var React = require("react");
var core_1 = require("../../core");
var resources_1 = require("../resources");
var fluentui_color_picker_1 = require("./fluentui_color_picker");
var color_space_picker_1 = require("./color_space_picker");
var tabs_view_1 = require("./tabs_view");
var object_list_editor_1 = require("../views/panels/object_list_editor");
var controls_1 = require("../views/panels/widgets/controls");
var react_1 = require("@fluentui/react");
var fluent_ui_gradient_picker_1 = require("./fluent_ui_gradient_picker");
var GradientPicker = /** @class */ (function (_super) {
    __extends(GradientPicker, _super);
    function GradientPicker(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            currentTab: "palettes",
            currentGradient: _this.props.defaultValue || {
                colorspace: fluent_ui_gradient_picker_1.Colorspace.LAB,
                colors: [
                    { r: 0, g: 0, b: 0 },
                    { r: 255, g: 255, b: 255 },
                ],
            },
            isPickerOpen: false,
            currentItemId: "",
            currentColor: null,
            currentItemIdx: null,
        };
        return _this;
    }
    GradientPicker.prototype.selectGradient = function (gradient, emit) {
        var _this = this;
        if (emit === void 0) { emit = false; }
        this.setState({
            currentGradient: gradient,
        }, function () {
            if (emit) {
                if (_this.props.onPick) {
                    _this.props.onPick(gradient);
                }
            }
        });
    };
    GradientPicker.prototype.renderGradientPalettes = function () {
        var e_1, _a;
        var _this = this;
        var items = resources_1.predefinedPalettes.filter(function (x) { return x.type == "sequential" || x.type == "diverging"; });
        var groups = [];
        var group2Index = new Map();
        try {
            for (var items_1 = __values(items), items_1_1 = items_1.next(); !items_1_1.done; items_1_1 = items_1.next()) {
                var p = items_1_1.value;
                var groupName = p.name.split("/")[0];
                var group = void 0;
                if (group2Index.has(groupName)) {
                    group = groups[group2Index.get(groupName)][1];
                }
                else {
                    group = [];
                    group2Index.set(groupName, groups.length);
                    groups.push([groupName, group]);
                }
                group.push(p);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (items_1_1 && !items_1_1.done && (_a = items_1.return)) _a.call(items_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return (React.createElement("section", { className: "palettes" },
            React.createElement("ul", null, groups.map(function (group, index) {
                return (React.createElement("li", { key: "m" + index },
                    React.createElement("div", { className: "label" }, group[0]),
                    React.createElement("ul", null, group[1].map(function (x) {
                        var gradient = {
                            colors: x.colors[0],
                            colorspace: fluent_ui_gradient_picker_1.Colorspace.LAB,
                        };
                        return (React.createElement("li", { key: x.name, className: "item", onClick: function () { return _this.selectGradient(gradient, true); } },
                            React.createElement(GradientView, { gradient: gradient }),
                            React.createElement("label", null, x.name.split("/")[1])));
                    }))));
            }))));
    };
    GradientPicker.prototype.changeColorPickerState = function (id, color, idx) {
        this.setState(__assign(__assign({}, this.state), { isPickerOpen: !this.state.isPickerOpen, currentItemId: id, currentColor: color, currentItemIdx: idx }));
    };
    GradientPicker.prototype.renderColorPicker = function () {
        var _this = this;
        return (React.createElement(React.Fragment, null, this.state.isPickerOpen && (React.createElement(react_1.Callout, { target: "#" + this.state.currentItemId, onDismiss: function () {
                return _this.changeColorPickerState(_this.state.currentItemId, null, null);
            }, alignTargetEdge: true },
            React.createElement(fluentui_color_picker_1.ColorPicker, { defaultValue: this.state.currentColor, onPick: function (color) {
                    var newGradient = core_1.deepClone(_this.state.currentGradient);
                    newGradient.colors[_this.state.currentItemIdx] = color;
                    _this.selectGradient(newGradient, true);
                }, parent: this })))));
    };
    // eslint-disable-next-line
    GradientPicker.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", { className: "gradient-picker" },
            React.createElement(tabs_view_1.TabsView, { tabs: GradientPicker.tabs, currentTab: this.state.currentTab, onSelect: function (tab) { return _this.setState({ currentTab: tab }); } }),
            this.state.currentTab == "palettes"
                ? this.renderGradientPalettes()
                : null,
            this.state.currentTab == "custom" ? (React.createElement("section", { className: "gradient-editor" },
                React.createElement("div", { className: "row" },
                    React.createElement(GradientView, { gradient: this.state.currentGradient })),
                React.createElement("div", { className: "colors-scroll" },
                    React.createElement(object_list_editor_1.ReorderListView, { enabled: true, onReorder: function (dragIndex, dropIndex) {
                            var newGradient = core_1.deepClone(_this.state.currentGradient);
                            object_list_editor_1.ReorderListView.ReorderArray(newGradient.colors, dragIndex, dropIndex);
                            _this.selectGradient(newGradient, true);
                        } },
                        this.state.currentGradient.colors.map(function (color, i) {
                            return (React.createElement("div", { className: "color-row", key: "m" + i },
                                React.createElement("span", { id: "color_" + i, className: "color-item", style: { background: fluentui_color_picker_1.colorToCSS(color) }, onClick: function () {
                                        _this.changeColorPickerState("color_" + i, color, i);
                                    } }),
                                React.createElement(color_space_picker_1.InputField, { defaultValue: core_1.colorToHTMLColorHEX(color), onEnter: function (value) {
                                        var newColor = core_1.colorFromHTMLColor(value);
                                        var newGradient = core_1.deepClone(_this.state.currentGradient);
                                        newGradient.colors[i] = newColor;
                                        _this.selectGradient(newGradient, true);
                                        return true;
                                    } }),
                                React.createElement(controls_1.Button, { icon: "ChromeClose", onClick: function () {
                                        if (_this.state.currentGradient.colors.length > 1) {
                                            var newGradient = core_1.deepClone(_this.state.currentGradient);
                                            newGradient.colors.splice(i, 1);
                                            _this.selectGradient(newGradient, true);
                                        }
                                    } })));
                        }),
                        this.renderColorPicker())),
                React.createElement("div", { className: "row" },
                    React.createElement(controls_1.Button, { icon: "general/plus", text: "Add", onClick: function () {
                            var newGradient = core_1.deepClone(_this.state.currentGradient);
                            newGradient.colors.push({ r: 150, g: 150, b: 150 });
                            _this.selectGradient(newGradient, true);
                        } }),
                    " ",
                    React.createElement(controls_1.Button, { icon: "Sort", text: "Reverse", onClick: function () {
                            var newGradient = core_1.deepClone(_this.state.currentGradient);
                            newGradient.colors.reverse();
                            _this.selectGradient(newGradient, true);
                        } }),
                    " ",
                    React.createElement(react_1.Dropdown, { options: [
                            { key: fluent_ui_gradient_picker_1.Colorspace.HCL, text: "HCL" },
                            { key: fluent_ui_gradient_picker_1.Colorspace.LAB, text: "Lab" },
                        ], onChange: function (event, option) {
                            if (option) {
                                var newGradient = core_1.deepClone(_this.state.currentGradient);
                                newGradient.colorspace = option.key;
                                _this.selectGradient(newGradient, true);
                            }
                        } })))) : null));
    };
    GradientPicker.tabs = [
        { name: "palettes", label: "Palettes" },
        { name: "custom", label: "Custom" },
    ];
    return GradientPicker;
}(React.Component));
exports.GradientPicker = GradientPicker;
var GradientView = /** @class */ (function (_super) {
    __extends(GradientView, _super);
    function GradientView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GradientView.prototype.componentDidMount = function () {
        this.componentDidUpdate();
    };
    GradientView.prototype.componentDidUpdate = function () {
        var _this = this;
        // Chrome doesn't like get/putImageData in this method
        // Doing so will cause the popup editor to not layout, although any change in its style will fix
        setTimeout(function () {
            if (!_this.refCanvas || !_this.props.gradient) {
                return;
            }
            var ctx = _this.refCanvas.getContext("2d");
            var width = _this.refCanvas.width;
            var height = _this.refCanvas.height;
            var scale = core_1.interpolateColors(_this.props.gradient.colors, _this.props.gradient.colorspace);
            var data = ctx.getImageData(0, 0, width, height);
            for (var i = 0; i < data.width; i++) {
                var t = i / (data.width - 1);
                var c = scale(t);
                for (var y = 0; y < data.height; y++) {
                    var ptr = (i + y * data.width) * 4;
                    data.data[ptr++] = c.r;
                    data.data[ptr++] = c.g;
                    data.data[ptr++] = c.b;
                    data.data[ptr++] = 255;
                }
            }
            ctx.putImageData(data, 0, 0);
        }, 0);
    };
    GradientView.prototype.render = function () {
        var _this = this;
        return (React.createElement("span", { className: "gradient-view" },
            React.createElement("canvas", { ref: function (e) { return (_this.refCanvas = e); }, width: 50, height: 2 })));
    };
    return GradientView;
}(React.PureComponent));
exports.GradientView = GradientView;
//# sourceMappingURL=gradient_picker.js.map