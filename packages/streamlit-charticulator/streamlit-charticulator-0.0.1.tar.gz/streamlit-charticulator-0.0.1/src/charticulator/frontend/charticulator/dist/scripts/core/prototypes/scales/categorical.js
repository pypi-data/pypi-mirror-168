"use strict";
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
exports.CategoricalScaleBase64Image = exports.CategoricalScaleImage = exports.CategoricalScaleBoolean = exports.CategoricalScaleEnum = exports.CategoricalScaleColor = exports.CategoricalScaleNumber = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var common_1 = require("../../common");
var solver_1 = require("../../solver");
var specification_1 = require("../../specification");
var index_1 = require("./index");
var d3_color_1 = require("d3-color");
var types_1 = require("../../specification/types");
var categorical_legend_1 = require("../legends/categorical_legend");
var strings_1 = require("../../../strings");
function reuseMapping(domain, existing) {
    var e_1, _a;
    var result = {};
    var available = [];
    try {
        for (var _b = __values(Object.keys(existing)), _c = _b.next(); !_c.done; _c = _b.next()) {
            var d = _c.value;
            if (domain.has(d)) {
                // Found one with the same key, reuse the color
                result[d] = existing[d];
            }
            else {
                // Other, make the color available
                available.push(existing[d]);
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
        }
        finally { if (e_1) throw e_1.error; }
    }
    // Assign remaining keys from the domain
    domain.forEach(function (v, d) {
        if (!Object.prototype.hasOwnProperty.call(result, d)) {
            if (available.length > 0) {
                result[d] = available[0];
                available.splice(0, 1);
            }
            else {
                // No available color left, fail
                return null;
            }
        }
    });
    return result;
}
var CategoricalScaleNumber = /** @class */ (function (_super) {
    __extends(CategoricalScaleNumber, _super);
    function CategoricalScaleNumber() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = ["rangeScale"];
        _this.attributes = {
            rangeScale: {
                name: "rangeScale",
                type: specification_1.AttributeType.Number,
            },
        };
        return _this;
    }
    CategoricalScaleNumber.prototype.mapDataToAttribute = function (data) {
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var number = props.mapping[data ? data === null || data === void 0 ? void 0 : data.toString() : null];
        return (number !== null && number !== void 0 ? number : 0) * attrs.rangeScale;
    };
    CategoricalScaleNumber.prototype.buildConstraint = function (data, target, solver) {
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var k = props.mapping[data === null || data === void 0 ? void 0 : data.toString()];
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[1, target]], [[k, solver.attr(attrs, "rangeScale")]]);
    };
    CategoricalScaleNumber.prototype.initializeState = function () {
        var attrs = this.state.attributes;
        attrs.rangeScale = 10;
    };
    CategoricalScaleNumber.prototype.inferParameters = function (column, options) {
        if (options === void 0) { options = {}; }
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var s = new common_1.Scale.CategoricalScale();
        var values = column.filter(function (x) { return typeof x == "string"; });
        s.inferParameters(values, types_1.OrderMode.order);
        props.mapping = {};
        var range = [1, s.domain.size];
        if (options.rangeNumber) {
            range = options.rangeNumber;
        }
        s.domain.forEach(function (v, d) {
            props.mapping[d] =
                (v / (s.domain.size - 1)) * (range[1] - range[0]) + range[0];
        });
        attrs.rangeScale = range[1];
    };
    CategoricalScaleNumber.prototype.getAttributePanelWidgets = function (manager) {
        var props = this.object.properties;
        var keys = [];
        for (var key in props.mapping) {
            if (Object.prototype.hasOwnProperty.call(props.mapping, key)) {
                keys.push(key);
            }
        }
        return [
            manager.sectionHeader(strings_1.strings.objects.scales.numberMapping),
            manager.scrollList(keys.map(function (key) {
                return manager.horizontal([2, 3], manager.text(key, "right"), manager.inputNumber({ property: "mapping", field: key }));
            })),
            manager.sectionHeader(strings_1.strings.objects.scales.exportProperties),
            manager.row("", manager.vertical(manager.inputBoolean({
                property: "autoDomainMin",
            }, {
                type: "checkbox",
                label: strings_1.strings.objects.scales.autoMin,
            }), manager.inputBoolean({
                property: "autoDomainMax",
            }, {
                type: "checkbox",
                label: strings_1.strings.objects.scales.autoMax,
            }))),
        ];
    };
    CategoricalScaleNumber.classID = "scale.categorical<string,number>";
    CategoricalScaleNumber.type = "scale";
    CategoricalScaleNumber.defaultProperties = {
        exposed: true,
        autoDomainMin: true,
        autoDomainMax: true,
    };
    return CategoricalScaleNumber;
}(index_1.ScaleClass));
exports.CategoricalScaleNumber = CategoricalScaleNumber;
var CategoricalScaleColor = /** @class */ (function (_super) {
    __extends(CategoricalScaleColor, _super);
    function CategoricalScaleColor() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = [];
        _this.attributes = {};
        return _this;
    }
    CategoricalScaleColor.prototype.mapDataToAttribute = function (data) {
        var props = this.object.properties;
        return props.mapping[data === null || data === void 0 ? void 0 : data.toString()];
    };
    // eslint-disable-next-line
    CategoricalScaleColor.prototype.initializeState = function () { };
    CategoricalScaleColor.prototype.inferParameters = function (column, options) {
        if (options === void 0) { options = {}; }
        var props = this.object.properties;
        var s = new common_1.Scale.CategoricalScale();
        var values = column.filter(function (x) { return x != null; }).map(function (x) { return x.toString(); });
        s.inferParameters(values, types_1.OrderMode.order);
        props.autoDomainMin = true;
        props.autoDomainMax = true;
        // If we shouldn't reuse the range, then reset the mapping
        if (!options.reuseRange) {
            props.mapping = null;
            // Otherwise, if we already have a mapping, try to reuse it
        }
        else if (props.mapping != null) {
            if (options.extendScaleMin || options.extendScaleMax) {
                var mapping_1 = reuseMapping(s.domain, props.mapping);
                var colorList_1 = literalColorValues(values);
                if (!colorList_1) {
                    // Find a good default color palette
                    colorList_1 = common_1.getDefaultColorPalette(s.length);
                }
                s.domain.forEach(function (v, d) {
                    // If we still don't have enough colors, reuse them
                    // NEEDTO: fix this with a better method
                    if (!mapping_1[d]) {
                        mapping_1[d] = colorList_1[v % colorList_1.length];
                    }
                });
                // Find unused mapping and save them, if count if new mapping domain is less thant old.
                var newMappingKeys = Object.keys(mapping_1);
                var oldMappingKeys = Object.keys(props.mapping);
                if (newMappingKeys.length < oldMappingKeys.length) {
                    oldMappingKeys
                        .slice(newMappingKeys.length, oldMappingKeys.length)
                        .filter(function (key) { return key.startsWith(categorical_legend_1.ReservedMappingKeyNamePrefix); })
                        .forEach(function (key) {
                        mapping_1[key] = props.mapping[key];
                    });
                }
                props.mapping = mapping_1;
            }
            else {
                props.mapping = reuseMapping(s.domain, props.mapping);
            }
        }
        if (props.mapping == null) {
            // If we can't reuse existing colors, infer from scratch
            props.mapping = {};
            // try to use literal values as color
            var colorList_2 = literalColorValues(values);
            if (colorList_2) {
                s.domain.forEach(function (v, d) {
                    props.mapping[d] = colorList_2[v % colorList_2.length];
                });
            }
            else if (common_1.getDefaultColorPaletteGenerator()) {
                s.domain.forEach(function (v, d) {
                    props.mapping[d] = common_1.getDefaultColorPaletteByValue(d);
                });
            }
            else {
                colorList_2 = common_1.getDefaultColorPalette(s.length);
                s.domain.forEach(function (v, d) {
                    props.mapping[d] = colorList_2[v % colorList_2.length];
                });
            }
        }
    };
    CategoricalScaleColor.prototype.getAttributePanelWidgets = function (manager) {
        var props = this.object.properties;
        var keys = [];
        for (var key in props.mapping) {
            if (Object.prototype.hasOwnProperty.call(props.mapping, key)) {
                keys.push(key);
            }
        }
        return [
            manager.inputBoolean([
                {
                    property: "autoDomainMin",
                },
                {
                    property: "autoDomainMax",
                },
            ], {
                type: "checkbox",
                label: strings_1.strings.objects.dataAxis.autoUpdateValues,
            }),
            manager.sectionHeader(strings_1.strings.objects.scales.colorMapping),
            manager.scrollList(keys.map(function (key) {
                return manager.horizontal([1, 0], manager.inputText({ property: "mapping" }, {
                    updateProperty: true,
                    value: key,
                    underline: true,
                    styles: {
                        textAlign: "right",
                    },
                    emitMappingAction: true,
                }), manager.inputColor({
                    property: "mapping",
                    field: key,
                    noComputeLayout: true,
                }, {
                    // label: key,
                    noDefaultMargin: true,
                    stopPropagation: true,
                    labelKey: key,
                    width: 100,
                    underline: true,
                    pickerBeforeTextField: true,
                    styles: {
                        marginTop: "0px",
                    },
                }));
            })),
        ];
    };
    CategoricalScaleColor.metadata = {
        displayName: "Scale",
        iconPath: "scale/color",
    };
    CategoricalScaleColor.classID = "scale.categorical<string,color>";
    CategoricalScaleColor.type = "scale";
    return CategoricalScaleColor;
}(index_1.ScaleClass));
exports.CategoricalScaleColor = CategoricalScaleColor;
function literalColorValues(values) {
    var colorList = [];
    var cache = {};
    for (var i = 0; i < values.length; i++) {
        var value = values[i];
        if (cache[value]) {
            continue;
        }
        var d3c = d3_color_1.color(value);
        if (!d3c) {
            return null;
        }
        var _a = d3c.rgb(), r = _a.r, g = _a.g, b = _a.b, opacity = _a.opacity;
        if (opacity !== 1) {
            return null;
        }
        colorList.push({ r: r, g: g, b: b });
        cache[value] = true;
    }
    return colorList;
}
var CategoricalScaleEnum = /** @class */ (function (_super) {
    __extends(CategoricalScaleEnum, _super);
    function CategoricalScaleEnum() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = [];
        _this.attributes = {};
        return _this;
    }
    CategoricalScaleEnum.prototype.mapDataToAttribute = function (data) {
        var props = this.object.properties;
        return props.mapping[data === null || data === void 0 ? void 0 : data.toString()];
    };
    // eslint-disable-next-line
    CategoricalScaleEnum.prototype.initializeState = function () { };
    CategoricalScaleEnum.prototype.inferParameters = function (column, options) {
        if (options === void 0) { options = {}; }
        var props = this.object.properties;
        var s = new common_1.Scale.CategoricalScale();
        var values = column.filter(function (x) { return x != null; }).map(function (x) { return x.toString(); });
        s.inferParameters(values, types_1.OrderMode.order);
        // If we shouldn't reuse the range, then reset the mapping
        if (!options.reuseRange) {
            props.mapping = null;
            // Otherwise, if we already have a mapping, try to reuse it
        }
        else if (props.mapping != null) {
            props.mapping = reuseMapping(s.domain, props.mapping);
        }
        if (props.mapping == null) {
            props.mapping = {};
            if (options.rangeEnum) {
                props.defaultRange = options.rangeEnum.slice();
            }
            s.domain.forEach(function (v, d) {
                if (options.rangeEnum) {
                    props.mapping[d] = options.rangeEnum[v % options.rangeEnum.length];
                }
                else {
                    props.mapping[d] = d;
                }
            });
        }
    };
    CategoricalScaleEnum.prototype.getAttributePanelWidgets = function (manager) {
        var props = this.object.properties;
        var keys = [];
        for (var key in props.mapping) {
            if (Object.prototype.hasOwnProperty.call(props.mapping, key)) {
                keys.push(key);
            }
        }
        return [
            manager.sectionHeader(strings_1.strings.objects.scales.stringMapping),
            manager.scrollList(keys.map(function (key) {
                return manager.horizontal([2, 3], manager.inputText({ property: "mapping" }, {
                    updateProperty: true,
                    value: key,
                    underline: true,
                    styles: {
                        textAlign: "right",
                    },
                }), manager.inputComboBox({ property: "mapping", field: key }, {
                    defaultRange: props.defaultRange,
                    valuesOnly: false,
                }));
            })),
        ];
    };
    CategoricalScaleEnum.classID = "scale.categorical<string,enum>";
    CategoricalScaleEnum.type = "scale";
    return CategoricalScaleEnum;
}(index_1.ScaleClass));
exports.CategoricalScaleEnum = CategoricalScaleEnum;
var CategoricalScaleBoolean = /** @class */ (function (_super) {
    __extends(CategoricalScaleBoolean, _super);
    function CategoricalScaleBoolean() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = [];
        _this.attributes = {};
        return _this;
    }
    CategoricalScaleBoolean.prototype.mapDataToAttribute = function (data) {
        var props = this.object.properties;
        return props.mapping[data === null || data === void 0 ? void 0 : data.toString()];
    };
    // eslint-disable-next-line
    CategoricalScaleBoolean.prototype.initializeState = function () { };
    CategoricalScaleBoolean.prototype.inferParameters = function (column, options) {
        if (options === void 0) { options = {}; }
        var props = this.object.properties;
        var s = new common_1.Scale.CategoricalScale();
        var values = column.filter(function (x) { return x != null; }).map(function (x) { return x.toString(); });
        s.inferParameters(values, types_1.OrderMode.order);
        // If we shouldn't reuse the range, then reset the mapping
        if (!options.reuseRange) {
            props.mapping = null;
            // Otherwise, if we already have a mapping, try to reuse it
        }
        else if (props.mapping != null) {
            props.mapping = reuseMapping(s.domain, props.mapping);
        }
        if (props.mapping == null) {
            props.mapping = {};
            s.domain.forEach(function (v, d) {
                props.mapping[d] = true;
            });
        }
    };
    CategoricalScaleBoolean.prototype.getAttributePanelWidgets = function (manager) {
        var items = [];
        var props = this.object.properties;
        var mappingALL = {};
        var mappingNONE = {};
        for (var key in props.mapping) {
            if (Object.prototype.hasOwnProperty.call(props.mapping, key)) {
                items.push(manager.inputBoolean({ property: "mapping", field: key }, {
                    type: "checkbox-fill-width",
                    label: key,
                    styles: {
                        overflowX: "hidden",
                    },
                }));
                mappingALL[key] = true;
                mappingNONE[key] = false;
            }
        }
        return [
            manager.inputBoolean([
                {
                    property: "autoDomainMin",
                },
                {
                    property: "autoDomainMax",
                },
            ], {
                type: "checkbox",
                label: strings_1.strings.objects.dataAxis.autoUpdateValues,
            }),
            manager.sectionHeader(strings_1.strings.objects.scales.booleanMapping),
            manager.row(null, manager.horizontal([0, 0], manager.setButton({ property: "mapping" }, mappingALL, null, strings_1.strings.objects.scales.selectAll), manager.setButton({ property: "mapping" }, mappingNONE, null, strings_1.strings.objects.scales.clear))),
            manager.scrollList(items),
        ];
    };
    CategoricalScaleBoolean.classID = "scale.categorical<string,boolean>";
    CategoricalScaleBoolean.type = "scale";
    return CategoricalScaleBoolean;
}(index_1.ScaleClass));
exports.CategoricalScaleBoolean = CategoricalScaleBoolean;
var CategoricalScaleImage = /** @class */ (function (_super) {
    __extends(CategoricalScaleImage, _super);
    function CategoricalScaleImage() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = [];
        _this.attributes = {};
        return _this;
    }
    CategoricalScaleImage.prototype.mapDataToAttribute = function (data) {
        var props = this.object.properties;
        return props.mapping[data === null || data === void 0 ? void 0 : data.toString()];
    };
    // eslint-disable-next-line
    CategoricalScaleImage.prototype.initializeState = function () { };
    CategoricalScaleImage.prototype.inferParameters = function (column, options) {
        if (options === void 0) { options = {}; }
        var props = this.object.properties;
        var s = new common_1.Scale.CategoricalScale();
        var values = column.filter(function (x) { return x != null; }).map(function (x) { return x.toString(); });
        s.inferParameters(values, types_1.OrderMode.order);
        // If we shouldn't reuse the range, then reset the mapping
        if (!options.reuseRange) {
            props.mapping = null;
            // Otherwise, if we already have a mapping, try to reuse it
        }
        else if (props.mapping != null) {
            props.mapping = reuseMapping(s.domain, props.mapping);
        }
        if (props.mapping == null) {
            props.mapping = {};
            s.domain.forEach(function (v, d) {
                if (options.rangeImage) {
                    props.mapping[d] = options.rangeImage[v % options.rangeImage.length];
                }
                else {
                    props.mapping[d] = null;
                }
            });
        }
    };
    CategoricalScaleImage.prototype.getAttributePanelWidgets = function (manager) {
        var props = this.object.properties;
        var keys = [];
        for (var key in props.mapping) {
            if (Object.prototype.hasOwnProperty.call(props.mapping, key)) {
                keys.push(key);
            }
        }
        return [
            manager.inputBoolean([
                {
                    property: "autoDomainMin",
                },
                {
                    property: "autoDomainMax",
                },
            ], {
                type: "checkbox",
                label: strings_1.strings.objects.dataAxis.autoUpdateValues,
            }),
            manager.sectionHeader(strings_1.strings.objects.scales.imageMapping),
            manager.scrollList(keys.map(function (key) {
                return manager.horizontal([2, 5, 0], manager.inputText({ property: "mapping" }, {
                    updateProperty: true,
                    value: key,
                    underline: true,
                    styles: {
                        textAlign: "right",
                    },
                }), manager.inputImageProperty({ property: "mapping", field: key }), manager.clearButton({ property: "mapping", field: key }, "", true));
            }), {
                styles: {
                    paddingBottom: 5,
                    paddingTop: 5,
                },
            }),
        ];
    };
    CategoricalScaleImage.classID = "scale.categorical<string,image>";
    CategoricalScaleImage.type = "scale";
    return CategoricalScaleImage;
}(index_1.ScaleClass));
exports.CategoricalScaleImage = CategoricalScaleImage;
var CategoricalScaleBase64Image = /** @class */ (function (_super) {
    __extends(CategoricalScaleBase64Image, _super);
    function CategoricalScaleBase64Image() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = [];
        _this.attributes = {};
        return _this;
    }
    CategoricalScaleBase64Image.prototype.mapDataToAttribute = function (data) {
        var props = this.object.properties;
        return props.mapping[data === null || data === void 0 ? void 0 : data.toString()];
    };
    // eslint-disable-next-line
    CategoricalScaleBase64Image.prototype.initializeState = function () { };
    CategoricalScaleBase64Image.prototype.inferParameters = function (idColumn, options) {
        var props = this.object.properties;
        var s = new common_1.Scale.CategoricalScale();
        var idValues = idColumn.filter(function (x) { return x != null; }).map(function (x) { return x.toString(); });
        s.inferParameters(idValues, types_1.OrderMode.order);
        // If we shouldn't reuse the range, then reset the mapping
        if (!options.reuseRange) {
            props.mapping = null;
            // Otherwise, if we already have a mapping, try to reuse it
        }
        else if (props.mapping != null) {
            props.mapping = reuseMapping(s.domain, props.mapping);
        }
        if (props.mapping == null) {
            props.mapping = {};
            s.domain.forEach(function (v, d) {
                if (options.rangeImage) {
                    props.mapping[d] = options.rangeImage[v % options.rangeImage.length];
                }
                else {
                    props.mapping[d] = null;
                }
            });
        }
    };
    CategoricalScaleBase64Image.prototype.getAttributePanelWidgets = function (manager) {
        var props = this.object.properties;
        var keys = [];
        for (var key in props.mapping) {
            // eslint-disable-next-line
            if (props.mapping.hasOwnProperty(key)) {
                keys.push(key);
            }
        }
        return [
            manager.inputBoolean([
                {
                    property: "autoDomainMin",
                },
                {
                    property: "autoDomainMax",
                },
            ], {
                type: "checkbox",
                label: strings_1.strings.objects.dataAxis.autoUpdateValues,
            }),
            manager.sectionHeader(strings_1.strings.objects.scales.imageMapping),
            manager.scrollList(keys.map(function (key) {
                return manager.horizontal([2, 5], manager.inputText({ property: "mapping" }, {
                    updateProperty: true,
                    value: key,
                    underline: true,
                    styles: {
                        textAlign: "right",
                    },
                }), manager.inputImageProperty({ property: "mapping", field: key }), manager.clearButton({ property: "mapping", field: key }, "", true));
            }), {
                styles: {
                    paddingTop: 5,
                    paddingBottom: 5,
                },
            }),
        ];
    };
    CategoricalScaleBase64Image.classID = "scale.categorical<image,image>";
    CategoricalScaleBase64Image.type = "scale";
    return CategoricalScaleBase64Image;
}(index_1.ScaleClass));
exports.CategoricalScaleBase64Image = CategoricalScaleBase64Image;
//# sourceMappingURL=categorical.js.map