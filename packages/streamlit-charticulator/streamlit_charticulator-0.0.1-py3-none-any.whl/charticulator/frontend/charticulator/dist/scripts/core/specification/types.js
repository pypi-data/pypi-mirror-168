"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CollapseOrExpandPanels = exports.Colorspace = exports.TextAlignmentVertical = exports.TextAlignmentHorizontal = exports.TickFormatType = exports.NumericalMode = exports.AxisDataBindingType = exports.OrderMode = void 0;
var OrderMode;
(function (OrderMode) {
    OrderMode["alphabetically"] = "alphabetically";
    OrderMode["occurrence"] = "occurrence";
    OrderMode["order"] = "order";
})(OrderMode = exports.OrderMode || (exports.OrderMode = {}));
var AxisDataBindingType;
(function (AxisDataBindingType) {
    AxisDataBindingType["Default"] = "default";
    AxisDataBindingType["Numerical"] = "numerical";
    AxisDataBindingType["Categorical"] = "categorical";
})(AxisDataBindingType = exports.AxisDataBindingType || (exports.AxisDataBindingType = {}));
var NumericalMode;
(function (NumericalMode) {
    NumericalMode["Linear"] = "linear";
    NumericalMode["Logarithmic"] = "logarithmic";
    NumericalMode["Temporal"] = "temporal";
})(NumericalMode = exports.NumericalMode || (exports.NumericalMode = {}));
var TickFormatType;
(function (TickFormatType) {
    TickFormatType["None"] = "none";
    TickFormatType["Date"] = "date";
    TickFormatType["Number"] = "number";
})(TickFormatType = exports.TickFormatType || (exports.TickFormatType = {}));
var TextAlignmentHorizontal;
(function (TextAlignmentHorizontal) {
    TextAlignmentHorizontal["Left"] = "left";
    TextAlignmentHorizontal["Middle"] = "middle";
    TextAlignmentHorizontal["Right"] = "right";
})(TextAlignmentHorizontal = exports.TextAlignmentHorizontal || (exports.TextAlignmentHorizontal = {}));
var TextAlignmentVertical;
(function (TextAlignmentVertical) {
    TextAlignmentVertical["Top"] = "top";
    TextAlignmentVertical["Middle"] = "middle";
    TextAlignmentVertical["Bottom"] = "bottom";
})(TextAlignmentVertical = exports.TextAlignmentVertical || (exports.TextAlignmentVertical = {}));
var Colorspace;
(function (Colorspace) {
    Colorspace["Hcl"] = "hcl";
    Colorspace["Lab"] = "lab";
})(Colorspace = exports.Colorspace || (exports.Colorspace = {}));
var CollapseOrExpandPanels;
(function (CollapseOrExpandPanels) {
    CollapseOrExpandPanels["Collapse"] = "collapse";
    CollapseOrExpandPanels["Expand"] = "expand";
    CollapseOrExpandPanels["Custom"] = "custom";
})(CollapseOrExpandPanels = exports.CollapseOrExpandPanels || (exports.CollapseOrExpandPanels = {}));
//# sourceMappingURL=types.js.map