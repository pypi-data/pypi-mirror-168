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
Object.defineProperty(exports, "__esModule", { value: true });
exports.EmphasizableMarkClass = exports.DEFAULT_POWER_BI_OPACITY = exports.DEFAULT_EMPHASIS_STROKE_WIDTH = exports.DEFAULT_EMPHASIS_STROKE_COLOR = void 0;
var mark_1 = require("./mark");
var specification_1 = require("../../specification");
exports.DEFAULT_EMPHASIS_STROKE_COLOR = { r: 255, g: 0, b: 0 };
exports.DEFAULT_EMPHASIS_STROKE_WIDTH = 1;
exports.DEFAULT_POWER_BI_OPACITY = 0.4;
/**
 * Represents a mark class that is emphasizable
 */
var EmphasizableMarkClass = /** @class */ (function (_super) {
    __extends(EmphasizableMarkClass, _super);
    function EmphasizableMarkClass(parent, object, state, defaultMethod) {
        if (defaultMethod === void 0) { defaultMethod = specification_1.EmphasisMethod.Saturation; }
        var _this = _super.call(this, parent, object, state) || this;
        _this.defaultMethod = defaultMethod;
        return _this;
    }
    /**
     * Generates styling info for styling emphasized marks
     * @param emphasize If true, emphasis will be applied.
     */
    EmphasizableMarkClass.prototype.generateEmphasisStyle = function (emphasize) {
        var _a;
        // If emphasize is undefined (or true), we use full saturation
        var style = {
            saturation: 1,
        };
        // only if emphasize is explicitly false to we use saturation of .7
        var method = this.object.properties.emphasisMethod || this.defaultMethod;
        if (method === specification_1.EmphasisMethod.Saturation && emphasize === false) {
            var opacity = (_a = this.state.attributes) === null || _a === void 0 ? void 0 : _a.opacity;
            if (opacity > exports.DEFAULT_POWER_BI_OPACITY || !opacity) {
                style.opacity = exports.DEFAULT_POWER_BI_OPACITY;
            }
        }
        if (method === specification_1.EmphasisMethod.Outline && emphasize) {
            style.strokeColor = exports.DEFAULT_EMPHASIS_STROKE_COLOR;
            style.strokeWidth = exports.DEFAULT_EMPHASIS_STROKE_WIDTH;
        }
        return style;
    };
    return EmphasizableMarkClass;
}(mark_1.MarkClass));
exports.EmphasizableMarkClass = EmphasizableMarkClass;
//# sourceMappingURL=emphasis.js.map