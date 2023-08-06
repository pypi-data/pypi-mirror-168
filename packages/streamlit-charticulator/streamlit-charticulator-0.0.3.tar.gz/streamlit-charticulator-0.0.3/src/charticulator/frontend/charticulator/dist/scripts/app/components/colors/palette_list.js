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
exports.PaletteList = void 0;
var React = require("react");
var react_1 = require("@fluentui/react");
var styles_1 = require("./styles");
var PaletteList = /** @class */ (function (_super) {
    __extends(PaletteList, _super);
    function PaletteList() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PaletteList.prototype.render = function () {
        var e_1, _a;
        var _this = this;
        var palettes = this.props.palettes;
        var groups = [];
        var group2Index = new Map();
        try {
            for (var palettes_1 = __values(palettes), palettes_1_1 = palettes_1.next(); !palettes_1_1.done; palettes_1_1 = palettes_1.next()) {
                var p = palettes_1_1.value;
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
                if (palettes_1_1 && !palettes_1_1.done && (_a = palettes_1.return)) _a.call(palettes_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return (React.createElement("ul", null, groups.map(function (group, index) {
            return (React.createElement(React.Fragment, { key: "palette-group-wrapper-" + index },
                React.createElement(react_1.Label, { key: "palette-label-" + index }, group[0]),
                group[1].map(function (x) { return (React.createElement(react_1.DefaultButton, { key: x.name, onClick: function () { return _this.props.onClick(x); }, text: x.name.split("/")[1], styles: styles_1.defaultPaletteButtonsStyles, checked: _this.props.selected == x })); })));
        })));
    };
    return PaletteList;
}(React.PureComponent));
exports.PaletteList = PaletteList;
//# sourceMappingURL=palette_list.js.map