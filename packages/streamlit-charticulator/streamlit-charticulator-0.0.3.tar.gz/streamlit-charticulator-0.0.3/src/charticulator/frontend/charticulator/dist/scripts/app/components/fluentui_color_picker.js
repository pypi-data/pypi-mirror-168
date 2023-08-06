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
exports.ColorPicker = exports.colorToCSS = void 0;
var React = require("react");
var resources_1 = require("../resources");
var react_1 = require("@fluentui/react");
var color_grid_1 = require("./colors/color_grid");
var null_button_1 = require("./colors/null_button");
var color_pickers_1 = require("./colors/color_pickers");
var palette_list_1 = require("./colors/palette_list");
var app_store_1 = require("../stores/app_store");
var input_colors_pickers_1 = require("./colors/input_colors_pickers");
var styles_1 = require("./colors/styles");
function colorToCSS(color) {
    return "rgb(" + color.r.toFixed(0) + "," + color.g.toFixed(0) + "," + color.b.toFixed(0) + ")";
}
exports.colorToCSS = colorToCSS;
var ColorPicker = /** @class */ (function (_super) {
    __extends(ColorPicker, _super);
    function ColorPicker(props) {
        var e_1, _a, e_2, _b, e_3, _c;
        var _this = _super.call(this, props) || this;
        resources_1.addPowerBIThemeColors();
        if (_this.props.defaultValue) {
            var colorCSS = colorToCSS(_this.props.defaultValue);
            var matchedPalette = null;
            try {
                for (var _d = __values(resources_1.predefinedPalettes.filter(function (x) { return x.type == "palette"; })), _e = _d.next(); !_e.done; _e = _d.next()) {
                    var p = _e.value;
                    try {
                        for (var _f = (e_2 = void 0, __values(p.colors)), _g = _f.next(); !_g.done; _g = _f.next()) {
                            var g = _g.value;
                            try {
                                for (var g_1 = (e_3 = void 0, __values(g)), g_1_1 = g_1.next(); !g_1_1.done; g_1_1 = g_1.next()) {
                                    var c = g_1_1.value;
                                    if (colorToCSS(c) == colorCSS) {
                                        matchedPalette = p;
                                        break;
                                    }
                                }
                            }
                            catch (e_3_1) { e_3 = { error: e_3_1 }; }
                            finally {
                                try {
                                    if (g_1_1 && !g_1_1.done && (_c = g_1.return)) _c.call(g_1);
                                }
                                finally { if (e_3) throw e_3.error; }
                            }
                            if (matchedPalette) {
                                break;
                            }
                        }
                    }
                    catch (e_2_1) { e_2 = { error: e_2_1 }; }
                    finally {
                        try {
                            if (_g && !_g.done && (_b = _f.return)) _b.call(_f);
                        }
                        finally { if (e_2) throw e_2.error; }
                    }
                    if (matchedPalette) {
                        break;
                    }
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (_e && !_e.done && (_a = _d.return)) _a.call(_d);
                }
                finally { if (e_1) throw e_1.error; }
            }
            if (matchedPalette) {
                _this.state = {
                    currentPalette: matchedPalette,
                    currentPicker: null,
                    currentColor: _this.props.defaultValue,
                };
            }
            else {
                _this.state = {
                    currentPalette: null,
                    currentPicker: color_pickers_1.PickerType.HCL,
                    currentColor: _this.props.defaultValue,
                };
            }
        }
        else {
            _this.state = {
                currentPalette: resources_1.predefinedPalettes.filter(function (x) { return x.name == "Palette/ColorBrewer"; })[0],
                currentPicker: null,
            };
        }
        //REMOVE TO OPEN COLOR PALETTE BY DEFAULT VALUE
        //OPEN DEFAULT COLOR PALETTE
        _this.state = {
            currentPalette: resources_1.predefinedPalettes.filter(function (x) { return x.name == "Palette/ColorBrewer"; })[0],
            currentPicker: null,
            currentColor: _this.props.defaultValue,
        };
        return _this;
    }
    ColorPicker.prototype.render = function () {
        var _this = this;
        var _a, _b, _c;
        var editorType = (_c = (_b = (_a = this.props) === null || _a === void 0 ? void 0 : _a.store) === null || _b === void 0 ? void 0 : _b.editorType) !== null && _c !== void 0 ? _c : app_store_1.EditorType.Chart;
        var isWeb = editorType === app_store_1.EditorType.Chart || editorType === app_store_1.EditorType.Nested;
        var pickersSection = (React.createElement(React.Fragment, null,
            React.createElement(styles_1.PickersSectionWrapper, null,
                React.createElement(styles_1.PickersSection, null,
                    React.createElement(palette_list_1.PaletteList, { palettes: resources_1.predefinedPalettes.filter(function (x) { return x.type == "palette"; }), selected: this.state.currentPalette, onClick: function (p) {
                            var _a;
                            _this.setState({ currentPalette: p, currentPicker: null });
                            (_a = _this.props.parent) === null || _a === void 0 ? void 0 : _a.forceUpdate();
                        } }),
                    React.createElement(react_1.Label, null, "Color Picker"),
                    React.createElement(color_pickers_1.ColorPickerButton, { state: this.state, onClick: function () {
                            return _this.setState({
                                currentPalette: null,
                                currentPicker: color_pickers_1.PickerType.HCL,
                            });
                        }, type: color_pickers_1.PickerType.HCL }),
                    React.createElement(color_pickers_1.ColorPickerButton, { state: this.state, onClick: function () {
                            return _this.setState({
                                currentPalette: null,
                                currentPicker: color_pickers_1.PickerType.HSV,
                            });
                        }, type: color_pickers_1.PickerType.HSV })),
                React.createElement(null_button_1.NullButton, { allowNull: this.props.allowNull, onPick: this.props.onPick }))));
        var colorsSection = (React.createElement(styles_1.ColorsSectionWrapper, null,
            this.state.currentPalette != null ? (React.createElement(color_grid_1.ColorGrid, { colors: this.state.currentPalette.colors, defaultValue: this.state.currentColor, onClick: function (c) {
                    _this.props.onPick(c);
                    _this.setState({ currentColor: c });
                    if (_this.props.closePicker) {
                        _this.props.closePicker();
                    }
                } })) : null,
            this.state.currentPicker == color_pickers_1.PickerType.HCL ? (React.createElement(input_colors_pickers_1.HCLColorPicker, { defaultValue: this.state.currentColor || { r: 0, g: 0, b: 0 }, onChange: function (c) {
                    _this.props.onPick(c);
                    _this.setState({ currentColor: c });
                } })) : null,
            this.state.currentPicker == color_pickers_1.PickerType.HSV ? (React.createElement(input_colors_pickers_1.HSVColorPicker, { defaultValue: this.state.currentColor || { r: 0, g: 0, b: 0 }, onChange: function (c) {
                    _this.props.onPick(c);
                    _this.setState({ currentColor: c });
                } })) : null));
        return (React.createElement(React.Fragment, null,
            React.createElement(styles_1.ColorsPickerWrapper, null,
                React.createElement(styles_1.ColorsPickerLeftSectionWrapper, null, isWeb ? pickersSection : colorsSection),
                isWeb ? colorsSection : pickersSection)));
    };
    return ColorPicker;
}(React.Component));
exports.ColorPicker = ColorPicker;
//# sourceMappingURL=fluentui_color_picker.js.map