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
exports.GraphicalElementDisplay = exports.renderGraphicalElementSVG = exports.renderSVGDefs = exports.renderTransform = exports.renderSVGPath = exports.renderStyle = exports.renderColor = exports.applyColorFilter = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var core_1 = require("../../core");
var utils_1 = require("../utils");
var chart_component_1 = require("../../container/chart_component");
var links_1 = require("../../core/prototypes/links");
// adapted from https://stackoverflow.com/a/20820649
// probably useful
// function desaturate(color: Color, amount: number) {
//   const { r, g, b } = color;
//   const l = 0.3 * r + 0.6 * g + 0.1 * b;
//   return {
//     r: Math.min(r + amount * (l - r), 255),
//     g: Math.min(g + amount * (l - g), 255),
//     b: Math.min(b + amount * (l - b), 255),
//   };
// }
var srgb2lab = core_1.getColorConverter("sRGB", "lab");
var lab2srgb = core_1.getColorConverter("lab", "sRGB");
function modifyNumber(value, modifier) {
    if (modifier.set != null) {
        return modifier.set;
    }
    else {
        if (modifier.multiply != null) {
            value *= modifier.multiply;
        }
        if (modifier.add != null) {
            value += modifier.add;
        }
        if (modifier.pow != null) {
            value = Math.pow(value, modifier.pow);
        }
        return value;
    }
}
function applyColorFilter(color, colorFilter) {
    var _a = __read(srgb2lab(color.r, color.g, color.b), 3), L = _a[0], A = _a[1], B = _a[2];
    if (colorFilter.saturation) {
        var s = Math.sqrt(A * A + B * B);
        var sPrime = modifyNumber(s, colorFilter.saturation);
        if (s == 0) {
            A = 0;
            B = 0;
        }
        else {
            A *= sPrime / s;
            B *= sPrime / s;
        }
    }
    if (colorFilter.lightness) {
        L = modifyNumber(L / 100, colorFilter.lightness) * 100;
    }
    var _b = __read(lab2srgb(L, A, B), 3), r = _b[0], g = _b[1], b = _b[2];
    return { r: r, g: g, b: b };
}
exports.applyColorFilter = applyColorFilter;
/**
 * Coverts {@Color} to `rgb(r,g,b)` string. Or coverts `#RRGGBB` fromat to `rgb(r,g,b)`}
 * @param color {@Color} object or color string in HEX format (`#RRGGBB`)
 */
function renderColor(color, colorFilter) {
    if (!color) {
        return "rgb(0,0,0)";
    }
    if (typeof color === "string") {
        color = core_1.hexToRgb(color);
    }
    if (typeof color === "object") {
        if (colorFilter) {
            color = applyColorFilter(color, colorFilter);
        }
        return "rgb(" + color.r.toFixed(0) + "," + color.g.toFixed(0) + "," + color.b.toFixed(0) + ")";
    }
}
exports.renderColor = renderColor;
function renderStyle(style) {
    if (style == null) {
        return {};
    }
    return {
        stroke: style.strokeColor
            ? renderColor(style.strokeColor, style.colorFilter)
            : "none",
        strokeOpacity: style.strokeOpacity != undefined ? style.strokeOpacity : 1,
        strokeWidth: style.strokeWidth != undefined ? style.strokeWidth : 1,
        strokeLinecap: style.strokeLinecap != undefined ? style.strokeLinecap : "round",
        strokeLinejoin: style.strokeLinejoin != undefined ? style.strokeLinejoin : "round",
        fill: style.fillColor
            ? renderColor(style.fillColor, style.colorFilter)
            : "none",
        fillOpacity: style.fillOpacity != undefined ? style.fillOpacity : 1,
        textAnchor: style.textAnchor != undefined ? style.textAnchor : "start",
        opacity: style.opacity != undefined ? style.opacity : 1,
        strokeDasharray: style.strokeDasharray != undefined ? style.strokeDasharray : null,
    };
}
exports.renderStyle = renderStyle;
var path_commands = {
    M: function (args) { return "M " + utils_1.toSVGNumber(args[0]) + "," + utils_1.toSVGNumber(-args[1]); },
    L: function (args) { return "L " + utils_1.toSVGNumber(args[0]) + "," + utils_1.toSVGNumber(-args[1]); },
    C: function (args) {
        return "C " + utils_1.toSVGNumber(args[0]) + "," + utils_1.toSVGNumber(-args[1]) + "," + utils_1.toSVGNumber(args[2]) + "," + utils_1.toSVGNumber(-args[3]) + "," + utils_1.toSVGNumber(args[4]) + "," + utils_1.toSVGNumber(-args[5]);
    },
    Q: function (args) {
        return "Q " + utils_1.toSVGNumber(args[0]) + "," + utils_1.toSVGNumber(-args[1]) + "," + utils_1.toSVGNumber(args[2]) + "," + utils_1.toSVGNumber(-args[3]);
    },
    A: function (args) {
        return "A " + utils_1.toSVGNumber(args[0]) + "," + utils_1.toSVGNumber(args[1]) + "," + utils_1.toSVGNumber(args[2]) + "," + utils_1.toSVGNumber(args[3]) + "," + utils_1.toSVGNumber(args[4]) + "," + utils_1.toSVGNumber(args[5]) + "," + utils_1.toSVGNumber(-args[6]);
    },
    Z: function () { return "Z"; },
};
function renderSVGPath(cmds) {
    return cmds.map(function (x) { return path_commands[x.cmd](x.args); }).join(" ");
}
exports.renderSVGPath = renderSVGPath;
function renderTransform(transform) {
    if (!transform) {
        return null;
    }
    if (Math.abs(transform.angle) < 1e-7) {
        return "translate(" + utils_1.toSVGNumber(transform.x) + "," + utils_1.toSVGNumber(-transform.y) + ")";
    }
    else {
        return "translate(" + utils_1.toSVGNumber(transform.x) + "," + utils_1.toSVGNumber(-transform.y) + ") rotate(" + utils_1.toSVGNumber(-transform.angle) + ")";
    }
}
exports.renderTransform = renderTransform;
var TextOnPath = /** @class */ (function (_super) {
    __extends(TextOnPath, _super);
    function TextOnPath() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.pathID = core_1.uniqueID();
        return _this;
    }
    TextOnPath.prototype.render = function () {
        return (React.createElement("g", null,
            React.createElement("defs", null,
                React.createElement("path", { id: this.pathID, fill: "none", stroke: "red", d: renderSVGPath(this.props.cmds) })),
            React.createElement("text", { style: __assign(__assign({}, this.props.style), { textAnchor: this.props.align }) },
                React.createElement("textPath", { href: "#" + this.pathID, startOffset: this.props.align == "start"
                        ? "0%"
                        : this.props.align == "middle"
                            ? "50%"
                            : "100%" }, this.props.text))));
    };
    return TextOnPath;
}(React.PureComponent));
function renderEndSVGArrow(element) {
    var arrowElement;
    switch (element.endArrowType) {
        case links_1.ArrowType.NO_ARROW:
            return;
        case links_1.ArrowType.DIAMOND_ARROW:
            arrowElement = (React.createElement("path", { d: "M 5 0 L 10 5 L 5 10 L 0 5 z", fill: renderColor(element.style.strokeColor, element.style.colorFilter) }));
            break;
        case links_1.ArrowType.OVAL_ARROW:
            arrowElement = (React.createElement("circle", { cx: "5", cy: "5", r: "5", fill: renderColor(element.style.strokeColor, element.style.colorFilter) }));
            break;
        case links_1.ArrowType.ARROW:
        default:
            arrowElement = (React.createElement("path", { d: "M 0 0 L 10 5 L 0 10 z", fill: renderColor(element.style.strokeColor, element.style.colorFilter) }));
            break;
    }
    return (React.createElement("marker", { id: element.style.endArrowColorId, viewBox: "0 0 10 10", refX: "9", refY: "5", markerUnits: "strokeWidth", markerWidth: "10", markerHeight: "10", orient: "auto" }, arrowElement));
}
function renderStartSVGArrow(element) {
    var arrowElement;
    switch (element.beginArrowType) {
        case links_1.ArrowType.NO_ARROW:
            return;
        case links_1.ArrowType.DIAMOND_ARROW:
            arrowElement = (React.createElement("path", { d: "M 5 0 L 10 5 L 5 10 L 0 5 z", fill: renderColor(element.style.strokeColor, element.style.colorFilter) }));
            break;
        case links_1.ArrowType.OVAL_ARROW:
            arrowElement = (React.createElement("circle", { cx: "5", cy: "5", r: "5", fill: renderColor(element.style.strokeColor, element.style.colorFilter) }));
            break;
        case links_1.ArrowType.ARROW:
        default:
            arrowElement = (React.createElement("path", { d: "M 10 0 L 10 10 L 0 5 z", fill: renderColor(element.style.strokeColor, element.style.colorFilter) }));
            break;
    }
    return (React.createElement("marker", { id: element.style.startArrowColorId, viewBox: "0 0 10 10", refX: "1", refY: "5", markerUnits: "strokeWidth", markerWidth: "10", markerHeight: "10", orient: "auto" }, arrowElement));
}
function renderSVGDefs(element) {
    var _a;
    if (!element) {
        return null;
    }
    switch (element.type) {
        case "text": {
            var text = element;
            if (text.style.backgroundColor) {
                return (React.createElement("filter", { x: "0", y: "0", width: "1", height: "1", id: text.style.backgroundColorId },
                    React.createElement("feFlood", { floodColor: renderColor(text.style.backgroundColor, text.style.colorFilter), result: "bg", "flood-opacity": "0" }),
                    React.createElement("feMerge", null,
                        React.createElement("feMergeNode", { in: "bg" }),
                        React.createElement("feMergeNode", { in: "SourceGraphic" }))));
            }
            else {
                return null;
            }
        }
        case "path": {
            var path = element;
            return (React.createElement(React.Fragment, null,
                renderEndSVGArrow(path),
                renderStartSVGArrow(path)));
        }
        case "group": {
            var group = element;
            return (React.createElement(React.Fragment, null, (_a = group.elements) === null || _a === void 0 ? void 0 : _a.map(function (x, idx) {
                return (React.createElement(React.Fragment, { key: "SVGDefs-" + idx }, renderSVGDefs(x)));
            })));
        }
    }
}
exports.renderSVGDefs = renderSVGDefs;
/** The method renders all chart elements in SVG document */
// eslint-disable-next-line
function renderGraphicalElementSVG(element, options) {
    var _a;
    if (!element) {
        return null;
    }
    if (!options) {
        options = {};
    }
    var style = options.noStyle
        ? null
        : renderStyle(options.styleOverride || element.style);
    // OnClick event handler
    var mouseEvents = {};
    if (element.selectable) {
        style.cursor = "pointer";
        style.pointerEvents = "all";
        if (options.onClick) {
            mouseEvents.onClick = function (e) {
                e.stopPropagation();
                if (element.selectable.enableSelection ||
                    element.selectable.enableSelection === undefined) {
                    options.onClick(element.selectable, e.nativeEvent);
                }
            };
        }
        if (options.onMouseEnter) {
            mouseEvents.onMouseEnter = function (e) {
                if (element.selectable.enableTooltips ||
                    element.selectable.enableTooltips === undefined) {
                    options.onMouseEnter(element.selectable, e.nativeEvent);
                }
            };
        }
        if (options.onMouseLeave) {
            mouseEvents.onMouseLeave = function (e) {
                if (element.selectable.enableTooltips ||
                    element.selectable.enableTooltips === undefined) {
                    options.onMouseLeave(element.selectable, e.nativeEvent);
                }
            };
        }
        if (options.onContextMenu) {
            mouseEvents.onContextMenu = function (e) {
                e.stopPropagation();
                if (element.selectable.enableContextMenu ||
                    element.selectable.enableContextMenu === undefined) {
                    options.onContextMenu(element.selectable, e.nativeEvent);
                }
            };
        }
    }
    if (element.interactable) {
        if (element.interactable.onClick) {
            mouseEvents.onClick = element.interactable.onClick;
        }
        if (element.interactable.onMousedown) {
            mouseEvents.onMouseDown = element.interactable.onMousedown;
        }
        if (element.interactable.onMouseup) {
            mouseEvents.onMouseUp = element.interactable.onMouseup;
        }
        if (element.interactable.onMousewheel) {
            mouseEvents.onWheel = element.interactable.onMousewheel;
        }
        if (element.interactable.onMousemove) {
            mouseEvents.onMouseMove = element.interactable.onMousemove;
        }
    }
    switch (element.type) {
        case "rect": {
            var rect = element;
            return (React.createElement("rect", __assign({ key: options.key }, mouseEvents, { className: options.className || null, style: style, x: Math.min(rect.x1, rect.x2), y: -Math.max(rect.y1, rect.y2), width: Math.abs(rect.x1 - rect.x2), height: Math.abs(rect.y1 - rect.y2), rx: rect.rx, ry: rect.ry, transform: "rotate(" + ((_a = rect.rotation) !== null && _a !== void 0 ? _a : 0) + ")" })));
        }
        case "circle": {
            var circle = element;
            return (React.createElement("circle", __assign({ key: options.key }, mouseEvents, { className: options.className || null, style: style, cx: circle.cx, cy: -circle.cy, r: circle.r })));
        }
        case "ellipse": {
            var ellipse = element;
            return (React.createElement("ellipse", __assign({ key: options.key }, mouseEvents, { className: options.className || null, style: style, cx: (ellipse.x1 + ellipse.x2) / 2, cy: -(ellipse.y1 + ellipse.y2) / 2, rx: Math.abs(ellipse.x1 - ellipse.x2) / 2, ry: Math.abs(ellipse.y1 - ellipse.y2) / 2 })));
        }
        case "line": {
            var line = element;
            return (React.createElement("line", __assign({ key: options.key }, mouseEvents, { className: options.className || null, style: style, x1: line.x1, y1: -line.y1, x2: line.x2, y2: -line.y2 })));
        }
        case "polygon": {
            var polygon = element;
            return (React.createElement("polygon", __assign({ key: options.key }, mouseEvents, { className: options.className || null, style: style, points: polygon.points
                    .map(function (p) { return utils_1.toSVGNumber(p.x) + "," + utils_1.toSVGNumber(-p.y); })
                    .join(" ") })));
        }
        case "path": {
            var path = element;
            var d = renderSVGPath(path.cmds);
            var markerStart = path.beginArrowType != links_1.ArrowType.NO_ARROW
                ? "url(#" + path.style.startArrowColorId + ")"
                : null;
            var markerEnd = path.endArrowType != links_1.ArrowType.NO_ARROW
                ? "url(#" + path.style.endArrowColorId + ")"
                : null;
            return (React.createElement("path", __assign({ key: options.key }, mouseEvents, { className: options.className || null, style: style, d: d, transform: path.transform, markerEnd: markerEnd, markerStart: markerStart })));
        }
        case "text-on-path": {
            var text = element;
            style.fontFamily = text.fontFamily;
            style.fontSize = text.fontSize + "px";
            return (React.createElement(TextOnPath, { text: text.text, style: style, cmds: text.pathCmds, align: text.align }));
        }
        case "text": {
            var text = element;
            style.fontFamily = text.fontFamily;
            style.fontSize = text.fontSize + "px";
            var filter = text.style.backgroundColor
                ? "url(#" + text.style.backgroundColorId + ")"
                : null;
            if (style.stroke != "none") {
                var style2 = core_1.shallowClone(style);
                style2.fill = style.stroke;
                var e1 = (React.createElement("text", __assign({}, mouseEvents, { className: options.className || null, style: style2, x: text.cx, y: -text.cy, filter: filter }), text.text));
                style.stroke = "none";
                var e2 = (React.createElement("text", __assign({}, mouseEvents, { className: options.className || null, style: style, x: text.cx, y: -text.cy }), text.text));
                return (React.createElement("g", { key: options.key },
                    e1,
                    e2));
            }
            else {
                return (React.createElement("text", __assign({ key: options.key }, mouseEvents, { className: options.className || null, style: style, x: text.cx, y: -text.cy, filter: filter }), text.text));
            }
        }
        case "image": {
            var image = element;
            var preserveAspectRatio = null;
            switch (image.mode) {
                case "letterbox":
                    preserveAspectRatio = "meet";
                    break;
                case "stretch":
                    preserveAspectRatio = "none";
                    break;
            }
            return (React.createElement("image", __assign({ key: options.key }, mouseEvents, { className: options.className || null, style: style, preserveAspectRatio: preserveAspectRatio, xlinkHref: options.externalResourceResolver
                    ? options.externalResourceResolver(image.src)
                    : image.src, x: image.x, y: -image.y - image.height, width: image.width, height: image.height })));
        }
        case "chart-container": {
            var component_1 = element;
            var subSelection = options.selection
                ? {
                    isSelected: function (table, rowIndices) {
                        // Get parent row indices from component row indices
                        var parentRowIndices = rowIndices.map(function (x) { return component_1.selectable.rowIndices[x]; });
                        // Query the selection with parent row indices
                        return options.selection.isSelected(component_1.selectable.plotSegment.table, parentRowIndices);
                    },
                }
                : null;
            var convertEventHandler = function (handler) {
                if (!handler) {
                    return null;
                }
                return function (s, parameters) {
                    if (s == null) {
                        // Clicked inside the ChartComponent but not on a glyph,
                        // in this case we select the whole thing
                        handler(component_1.selectable, parameters);
                    }
                    else {
                        // Clicked on a glyph of ChartComponent (or a sub-component)
                        // in this case we translate the component's rowIndices its parent's
                        handler({
                            plotSegment: component_1.selectable.plotSegment,
                            glyphIndex: component_1.selectable.glyphIndex,
                            rowIndices: s.rowIndices.map(function (i) { return component_1.selectable.rowIndices[i]; }),
                        }, parameters);
                    }
                };
            };
            return (React.createElement(chart_component_1.ChartComponent, { key: options.key, chart: component_1.chart, dataset: component_1.dataset, width: component_1.width, height: component_1.height, rootElement: "g", sync: options.chartComponentSync, selection: subSelection, onGlyphClick: convertEventHandler(options.onClick), onGlyphMouseEnter: convertEventHandler(options.onMouseEnter), onGlyphMouseLeave: convertEventHandler(options.onMouseLeave), rendererOptions: {
                    chartComponentSync: options.chartComponentSync,
                    externalResourceResolver: options.externalResourceResolver,
                } }));
        }
        case "group": {
            var group = element;
            return (React.createElement("g", __assign({ transform: renderTransform(group.transform), key: group.key || options.key, style: {
                    opacity: group.style && group.style.opacity != null
                        ? group.style.opacity
                        : 1,
                } }, mouseEvents), group.elements.map(function (x, index) {
                return renderGraphicalElementSVG(x, {
                    key: "m" + index,
                    chartComponentSync: options.chartComponentSync,
                    externalResourceResolver: options.externalResourceResolver,
                    onClick: options.onClick,
                    onMouseEnter: options.onMouseEnter,
                    onMouseLeave: options.onMouseLeave,
                    onContextMenu: options.onContextMenu,
                    selection: options.selection,
                });
            })));
        }
    }
}
exports.renderGraphicalElementSVG = renderGraphicalElementSVG;
var GraphicalElementDisplay = /** @class */ (function (_super) {
    __extends(GraphicalElementDisplay, _super);
    function GraphicalElementDisplay() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GraphicalElementDisplay.prototype.render = function () {
        return renderGraphicalElementSVG(this.props.element);
    };
    return GraphicalElementDisplay;
}(React.PureComponent));
exports.GraphicalElementDisplay = GraphicalElementDisplay;
//# sourceMappingURL=index.js.map