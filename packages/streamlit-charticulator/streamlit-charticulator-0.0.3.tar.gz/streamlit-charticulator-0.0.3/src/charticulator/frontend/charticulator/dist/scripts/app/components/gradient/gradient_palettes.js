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
exports.GradientView = exports.GradientPalettes = void 0;
var React = require("react");
var resources_1 = require("../../resources");
var styles_1 = require("./styles");
var react_1 = require("@fluentui/react");
var core_1 = require("../../../core");
var fluent_ui_gradient_picker_1 = require("../fluent_ui_gradient_picker");
var GradientPalettes = /** @class */ (function (_super) {
    __extends(GradientPalettes, _super);
    function GradientPalettes() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GradientPalettes.prototype.render = function () {
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
        return (React.createElement(styles_1.TabWrapper, null, groups.map(function (group, index) {
            return (React.createElement("div", { key: "group-section-" + index },
                React.createElement(react_1.Label, null, group[0]),
                group[1].map(function (x) {
                    var gradient = {
                        colors: x.colors[0],
                        colorspace: fluent_ui_gradient_picker_1.Colorspace.LAB,
                    };
                    return (React.createElement(styles_1.PalettesWrapper, { key: x.name, onClick: function () { return _this.props.selectGradient(gradient, true); } },
                        React.createElement(GradientView, { gradient: gradient }),
                        React.createElement(react_1.Label, { styles: styles_1.colorPalettesLabelStyles }, x.name.split("/")[1])));
                })));
        })));
    };
    return GradientPalettes;
}(React.Component));
exports.GradientPalettes = GradientPalettes;
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
        return (React.createElement(styles_1.ColorGradientWrapper, { className: "gradient-view" },
            React.createElement("canvas", { ref: function (e) { return (_this.refCanvas = e); }, height: 2, style: { width: "100%" } })));
    };
    return GradientView;
}(React.PureComponent));
exports.GradientView = GradientView;
//# sourceMappingURL=gradient_palettes.js.map