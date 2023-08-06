"use strict";
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.AttrBuilder = void 0;
var specification_1 = require("../specification");
var AttrBuilder = /** @class */ (function () {
    function AttrBuilder() {
    }
    AttrBuilder.attr = function (name, type, options) {
        if (options === void 0) { options = {}; }
        var r = {};
        r[name] = __assign({ name: name, type: type }, options);
        return r;
    };
    AttrBuilder.number = function (name, solvable, options) {
        if (solvable === void 0) { solvable = true; }
        if (options === void 0) { options = {}; }
        if (solvable) {
            return this.attr(name, specification_1.AttributeType.Number, options);
        }
        else {
            return this.attr(name, specification_1.AttributeType.Number, __assign({ solverExclude: true }, options));
        }
    };
    AttrBuilder.color = function (name, options) {
        if (options === void 0) { options = {}; }
        return this.attr(name, specification_1.AttributeType.Color, __assign({ solverExclude: true }, options));
    };
    AttrBuilder.boolean = function (name, options) {
        if (options === void 0) { options = {}; }
        return this.attr(name, specification_1.AttributeType.Boolean, __assign({ solverExclude: true }, options));
    };
    AttrBuilder.enum = function (name, options) {
        if (options === void 0) { options = {}; }
        return this.attr(name, specification_1.AttributeType.Enum, __assign({ solverExclude: true }, options));
    };
    AttrBuilder.line = function () {
        return __assign(__assign(__assign(__assign({}, this.number("x1")), this.number("y1")), this.number("x2")), this.number("y2"));
    };
    AttrBuilder.point = function () {
        return __assign(__assign({}, this.number("x")), this.number("y"));
    };
    AttrBuilder.center = function () {
        return __assign(__assign({}, this.number("cx")), this.number("cy"));
    };
    AttrBuilder.size = function () {
        return __assign(__assign({}, this.number("width", true, { defaultRange: [0, 200] })), this.number("height", true, { defaultRange: [0, 200] }));
    };
    AttrBuilder.dXdY = function () {
        return __assign(__assign({}, this.number("dx", true, { defaultRange: [30, 100] })), this.number("dy", true, { defaultRange: [30, 100] }));
    };
    AttrBuilder.opacity = function () {
        return this.number("opacity", false, {
            defaultRange: [0, 1],
            defaultValue: 1,
        });
    };
    AttrBuilder.visible = function () {
        return this.boolean("visible", { defaultValue: true });
    };
    AttrBuilder.image = function () {
        return this.attr("image", specification_1.AttributeType.Image, {
            solverExclude: true,
            defaultValue: null,
        });
    };
    AttrBuilder.style = function (options) {
        if (options === void 0) { options = {}; }
        var r = __assign(__assign(__assign(__assign({}, this.color("stroke", { defaultValue: null })), this.number("strokeWidth", false, {
            defaultRange: [0, 5],
            defaultValue: 1,
        })), this.opacity()), this.visible());
        if (options.fill) {
            r.fill = this.color("fill", { defaultValue: null }).fill;
        }
        return r;
    };
    return AttrBuilder;
}());
exports.AttrBuilder = AttrBuilder;
//# sourceMappingURL=attrs.js.map