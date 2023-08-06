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
exports.ColorSpaceSelect = void 0;
var React = require("react");
var react_1 = require("@fluentui/react");
var fluentui_customized_components_1 = require("../../views/panels/widgets/controls/fluentui_customized_components");
var ColorSpaceSelect = /** @class */ (function (_super) {
    __extends(ColorSpaceSelect, _super);
    function ColorSpaceSelect() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ColorSpaceSelect.prototype.render = function () {
        var _this = this;
        var options = this.props.colorSpaces.map(function (x) {
            return { key: x.name, text: x.name };
        });
        return (React.createElement(react_1.ComboBox, { options: options, defaultSelectedKey: this.props.state.desc.name, onChange: function (event, option) {
                var e_1, _a;
                if (option) {
                    try {
                        for (var _b = __values(_this.props.colorSpaces), _c = _b.next(); !_c.done; _c = _b.next()) {
                            var sp = _c.value;
                            if (sp.name == option.key) {
                                var _d = __read(_this.props.state.desc.toRGB(_this.props.state.x1, _this.props.state.x2, _this.props.state.x3), 3), r = _d[0], g = _d[1], b = _d[2];
                                var _e = __read(sp.fromRGB(r, g, b), 3), x1 = _e[0], x2 = _e[1], x3 = _e[2];
                                _this.props.updateState({ desc: sp, x1: x1, x2: x2, x3: x3 });
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
                }
            }, styles: {
                root: __assign({}, fluentui_customized_components_1.defultComponentsHeight),
                input: {
                    width: "100px !important",
                },
            } }));
    };
    return ColorSpaceSelect;
}(React.Component));
exports.ColorSpaceSelect = ColorSpaceSelect;
//# sourceMappingURL=color_space_select.js.map