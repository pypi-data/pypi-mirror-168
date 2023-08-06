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
exports.registerClasses = exports.TableLinksClass = exports.LayoutsLinksClass = exports.SeriesLinksClass = exports.LinksClass = exports.facetRows = exports.ArrowType = exports.linkMarkTypes = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var common_1 = require("../../common");
var Graphics = require("../../graphics");
var Specification = require("../../specification");
var specification_1 = require("../../specification");
var chart_element_1 = require("../chart_element");
var object_1 = require("../object");
var strings_1 = require("../../../strings");
var utils_1 = require("./utils");
exports.linkMarkTypes = ["solid", "dashed", "dotted"];
var ArrowType;
(function (ArrowType) {
    ArrowType["NO_ARROW"] = "NO_ARROW";
    ArrowType["ARROW"] = "ARROW";
    ArrowType["DIAMOND_ARROW"] = "DIAMOND_ARROW";
    ArrowType["OVAL_ARROW"] = "OVAL_ARROW";
})(ArrowType = exports.ArrowType || (exports.ArrowType = {}));
function facetRows(table, indices, columns) {
    var e_1, _a;
    if (columns == null) {
        return [indices];
    }
    else {
        var facets = new common_1.MultistringHashMap();
        var _loop_1 = function (g) {
            var row = table.getGroupedContext(g);
            var facetValues = columns.map(function (c) { return c.getStringValue(row); });
            if (facets.has(facetValues)) {
                facets.get(facetValues).push(g);
            }
            else {
                facets.set(facetValues, [g]);
            }
        };
        try {
            for (var indices_1 = __values(indices), indices_1_1 = indices_1.next(); !indices_1_1.done; indices_1_1 = indices_1.next()) {
                var g = indices_1_1.value;
                _loop_1(g);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (indices_1_1 && !indices_1_1.done && (_a = indices_1.return)) _a.call(indices_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return Array.from(facets.values());
    }
}
exports.facetRows = facetRows;
var LinksClass = /** @class */ (function (_super) {
    __extends(LinksClass, _super);
    function LinksClass() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = ["color", "opacity"];
        _this.attributes = {
            linkMarkType: {
                name: "linkMarkType",
                type: Specification.AttributeType.Enum,
                solverExclude: true,
                defaultValue: "4 8",
                stateExclude: true,
                defaultRange: exports.linkMarkTypes,
            },
            color: {
                name: "color",
                type: Specification.AttributeType.Color,
                solverExclude: true,
                defaultValue: null,
                stateExclude: true,
            },
            strokeWidth: {
                name: "strokeWidth",
                type: Specification.AttributeType.Number,
                solverExclude: true,
                defaultValue: null,
                stateExclude: true,
            },
            opacity: {
                name: "opacity",
                type: Specification.AttributeType.Number,
                solverExclude: true,
                defaultValue: 1,
                defaultRange: [0, 1],
                stateExclude: true,
            },
        };
        return _this;
    }
    LinksClass.prototype.resolveLinkAnchorPoints = function (anchorPoints, glyph) {
        return anchorPoints.map(function (anchorPoint) {
            var pt = {
                anchorIndex: common_1.indexOf(glyph.marks, function (x) { return x.classID == "mark.anchor"; }),
                x: {
                    element: common_1.indexOf(glyph.marks, function (e) { return e._id == anchorPoint.x.element; }),
                    attribute: anchorPoint.x.attribute,
                },
                y: {
                    element: common_1.indexOf(glyph.marks, function (e) { return e._id == anchorPoint.y.element; }),
                    attribute: anchorPoint.y.attribute,
                },
                direction: anchorPoint.direction,
            };
            return pt;
        });
    };
    LinksClass.prototype.getAnchorPoints = function (renderState, anchorPoints, plotSegmentClass, glyphState, row) {
        var dx = glyphState.attributes.x;
        var dy = glyphState.attributes.y;
        var anchorIndex = anchorPoints[0].anchorIndex;
        dx -= glyphState.marks[anchorIndex].attributes.x;
        dy -= glyphState.marks[anchorIndex].attributes.y;
        var cs = plotSegmentClass.getCoordinateSystem();
        return {
            points: anchorPoints.map(function (pt) {
                var x = ((pt.x.element < 0
                    ? glyphState.attributes[pt.x.attribute]
                    : glyphState.marks[pt.x.element].attributes[pt.x.attribute]));
                var y = ((pt.y.element < 0
                    ? glyphState.attributes[pt.y.attribute]
                    : glyphState.marks[pt.y.element].attributes[pt.y.attribute]));
                var px = dx + x;
                var py = dy + y;
                return {
                    x: px,
                    y: py,
                    direction: pt.direction,
                };
            }),
            curveness: this.object.properties.curveness != null
                ? this.object.properties.curveness
                : 30,
            coordinateSystem: cs,
            color: renderState.colorFunction(row),
            opacity: renderState.opacityFunction(row),
            strokeWidth: renderState.strokeWidthFunction(row),
        };
    };
    LinksClass.BandPath = function (path, anchor, reversed, newPath) {
        if (reversed === void 0) { reversed = false; }
        if (newPath === void 0) { newPath = false; }
        var p0, p1;
        if (reversed) {
            p1 = anchor.points[0];
            p0 = anchor.points[1];
        }
        else {
            p0 = anchor.points[0];
            p1 = anchor.points[1];
        }
        if (newPath) {
            var p = Graphics.transform(anchor.coordinateSystem.getBaseTransform(), anchor.coordinateSystem.transformPoint(p0.x, p0.y));
            path.moveTo(p.x, p.y);
        }
        if (anchor.coordinateSystem instanceof Graphics.PolarCoordinates) {
            // let p = Graphics.transform(anchor.coordinateSystem.getBaseTransform(), anchor.coordinateSystem.transformPoint(p1.x, p1.y));
            path.polarLineTo(anchor.coordinateSystem.origin.x, anchor.coordinateSystem.origin.y, 90 - p0.x, p0.y, 90 - p1.x, p1.y);
        }
        else {
            var p = Graphics.transform(anchor.coordinateSystem.getBaseTransform(), anchor.coordinateSystem.transformPoint(p1.x, p1.y));
            path.lineTo(p.x, p.y);
        }
    };
    LinksClass.ConnectionPath = function (path, interpType, p1, d1, curveness1, p2, d2, curveness2, newPath) {
        if (newPath === void 0) { newPath = false; }
        if (newPath) {
            path.moveTo(p1.x, p1.y);
        }
        switch (interpType) {
            case "line":
                {
                    path.lineTo(p2.x, p2.y);
                }
                break;
            case "bezier":
                {
                    var dScaler1 = curveness1;
                    var dScaler2 = curveness2;
                    path.cubicBezierCurveTo(p1.x + d1.x * dScaler1, p1.y + d1.y * dScaler1, p2.x + d2.x * dScaler2, p2.y + d2.y * dScaler2, p2.x, p2.y);
                }
                break;
            case "circle": {
                var cx = (p1.x + p2.x) / 2, cy = (p1.y + p2.y) / 2;
                var dx = p1.y - p2.y, dy = p2.x - p1.x; // it doesn't matter if we normalize d or not
                if (Math.abs(d1.x * dx + d1.y * dy) < 1e-6) {
                    // Degenerate case, just a line from p1 to p2
                    path.lineTo(p2.x, p2.y);
                }
                else {
                    // Origin = c + d t
                    // Solve for t: d1 dot (c + t d - p) = 0
                    var t = (d1.x * (cx - p1.x) + d1.y * (cy - p1.y)) / (d1.x * dx + d1.y * dy);
                    var o = { x: cx - dx * t, y: cy - dy * t }; // the center of the circle
                    var r = common_1.Geometry.pointDistance(o, p1);
                    var scaler = 180 / Math.PI;
                    var angle1 = Math.atan2(p1.y - o.y, p1.x - o.x) * scaler;
                    var angle2 = Math.atan2(p2.y - o.y, p2.x - o.x) * scaler;
                    var sign = (p1.y - o.y) * d1.x - (p1.x - o.x) * d1.y;
                    if (sign > 0) {
                        while (angle2 > angle1) {
                            angle2 -= 360;
                        }
                    }
                    if (sign < 0) {
                        while (angle2 < angle1) {
                            angle2 += 360;
                        }
                    }
                    path.polarLineTo(o.x, o.y, angle1, r, angle2, r, false);
                }
            }
        }
    };
    // eslint-disable-next-line
    LinksClass.LinkPath = function (path, linkType, interpType, anchor1, anchor2) {
        switch (linkType) {
            case "line":
                {
                    var a1p0 = anchor1.coordinateSystem.transformPointWithBase(anchor1.points[0].x, anchor1.points[0].y);
                    var a2p0 = anchor2.coordinateSystem.transformPointWithBase(anchor2.points[0].x, anchor2.points[0].y);
                    var a1d0 = anchor1.coordinateSystem.transformDirectionAtPointWithBase(anchor1.points[0].x, anchor1.points[0].y, anchor1.points[0].direction.x, anchor1.points[0].direction.y);
                    var a2d0 = anchor2.coordinateSystem.transformDirectionAtPointWithBase(anchor2.points[0].x, anchor2.points[0].y, anchor2.points[0].direction.x, anchor2.points[0].direction.y);
                    LinksClass.ConnectionPath(path, interpType, a1p0, a1d0, anchor1.curveness, a2p0, a2d0, anchor2.curveness, true);
                }
                break;
            case "band":
                {
                    // Determine if we should reverse the band
                    var a1p0 = anchor1.coordinateSystem.transformPointWithBase(anchor1.points[0].x, anchor1.points[0].y);
                    var a1p1 = anchor1.coordinateSystem.transformPointWithBase(anchor1.points[1].x, anchor1.points[1].y);
                    var a2p0 = anchor2.coordinateSystem.transformPointWithBase(anchor2.points[0].x, anchor2.points[0].y);
                    var a2p1 = anchor2.coordinateSystem.transformPointWithBase(anchor2.points[1].x, anchor2.points[1].y);
                    var a1d0 = anchor1.coordinateSystem.transformDirectionAtPointWithBase(anchor1.points[0].x, anchor1.points[0].y, anchor1.points[0].direction.x, anchor1.points[0].direction.y);
                    var a1d1 = anchor1.coordinateSystem.transformDirectionAtPointWithBase(anchor1.points[1].x, anchor1.points[1].y, anchor1.points[1].direction.x, anchor1.points[1].direction.y);
                    var a2d0 = anchor2.coordinateSystem.transformDirectionAtPointWithBase(anchor2.points[0].x, anchor2.points[0].y, anchor2.points[0].direction.x, anchor2.points[0].direction.y);
                    var a2d1 = anchor2.coordinateSystem.transformDirectionAtPointWithBase(anchor2.points[1].x, anchor2.points[1].y, anchor2.points[1].direction.x, anchor2.points[1].direction.y);
                    var cross1 = common_1.Geometry.vectorCross(a1d0, {
                        x: a1p1.x - a1p0.x,
                        y: a1p1.y - a1p0.y,
                    });
                    var cross2 = common_1.Geometry.vectorCross(a2d0, {
                        x: a2p1.x - a2p0.x,
                        y: a2p1.y - a2p0.y,
                    });
                    var reverseBand = cross1 * cross2 > 0;
                    if (reverseBand) {
                        // anchor1[0] -> anchor1[1]
                        LinksClass.BandPath(path, anchor1, false, true);
                        // anchor1[1] -> anchor2[0]
                        LinksClass.ConnectionPath(path, interpType, a1p1, a1d1, anchor1.curveness, a2p0, a2d0, anchor2.curveness, false);
                        // anchor2[0] -> anchor2[1]
                        LinksClass.BandPath(path, anchor2, false, false);
                        // anchor2[1] -> anchor1[0]
                        LinksClass.ConnectionPath(path, interpType, a2p1, a2d1, anchor2.curveness, a1p0, a1d0, anchor1.curveness, false);
                        path.closePath();
                    }
                    else {
                        // anchor1[0] -> anchor1[1]
                        LinksClass.BandPath(path, anchor1, false, true);
                        // anchor1[1] -> anchor2[1]
                        LinksClass.ConnectionPath(path, interpType, a1p1, a1d1, anchor1.curveness, a2p1, a2d1, anchor2.curveness, false);
                        // anchor2[1] -> anchor2[0]
                        LinksClass.BandPath(path, anchor2, true, false);
                        // anchor2[0] -> anchor1[0]
                        LinksClass.ConnectionPath(path, interpType, a2p0, a2d0, anchor2.curveness, a1p0, a1d0, anchor1.curveness, false);
                        path.closePath();
                    }
                }
                break;
        }
    };
    // eslint-disable-next-line
    LinksClass.prototype.renderLinks = function (linkGraphics, lineType, anchorGroups, strokeDashArray) {
        var e_2, _a;
        var _b, _c;
        var props = this.object.properties;
        switch (linkGraphics) {
            case "line": {
                var beginArrowType_1 = (_b = props.beginArrowType) !== null && _b !== void 0 ? _b : ArrowType.NO_ARROW;
                var endArrowType_1 = (_c = props.endArrowType) !== null && _c !== void 0 ? _c : ArrowType.NO_ARROW;
                return Graphics.makeGroup(anchorGroups.map(function (anchors) {
                    var lines = [];
                    for (var i = 0; i < anchors.length - 1; i++) {
                        var path = Graphics.makePath({
                            strokeColor: anchors[i][0].color,
                            strokeOpacity: anchors[i][0].opacity,
                            strokeWidth: anchors[i][0].strokeWidth,
                            strokeDasharray: strokeDashArray,
                            strokeLinecap: "butt",
                            startArrowColorId: "start-arrow-color-id-" + common_1.getRandomNumber(),
                            endArrowColorId: "end-arrow-color-id-" + common_1.getRandomNumber(),
                        });
                        path.setBeginArrowType(beginArrowType_1);
                        path.setEndArrowType(endArrowType_1);
                        LinksClass.LinkPath(path, linkGraphics, lineType, anchors[i][0], anchors[i + 1][1]);
                        lines.push(path.path);
                    }
                    return Graphics.makeGroup(lines);
                }));
            }
            case "band": {
                var splitAnchors = true;
                if (splitAnchors) {
                    var map = new Map();
                    var hashAnchor = function (points) {
                        var dx = points[0].x - points[1].x;
                        var dy = points[0].y - points[1].y;
                        var dirX = points[0].direction.x;
                        var dirY = points[0].direction.y;
                        return [
                            points[0].x,
                            points[0].y,
                            points[1].x,
                            points[1].y,
                            Math.sign(dx * dirY - dy * dirX),
                        ].join(",");
                    };
                    try {
                        for (var anchorGroups_1 = __values(anchorGroups), anchorGroups_1_1 = anchorGroups_1.next(); !anchorGroups_1_1.done; anchorGroups_1_1 = anchorGroups_1.next()) {
                            var anchors = anchorGroups_1_1.value;
                            for (var i = 0; i < anchors.length - 1; i++) {
                                var a1 = anchors[i][0];
                                var a2 = anchors[i + 1][1];
                                var hash1 = hashAnchor(a1.points);
                                var hash2 = hashAnchor(a2.points);
                                if (map.has(hash1)) {
                                    map.get(hash1).push([a1, a2]);
                                }
                                else {
                                    map.set(hash1, [[a1, a2]]);
                                }
                                if (map.has(hash2)) {
                                    map.get(hash2).push([a2, a1]);
                                }
                                else {
                                    map.set(hash2, [[a2, a1]]);
                                }
                            }
                        }
                    }
                    catch (e_2_1) { e_2 = { error: e_2_1 }; }
                    finally {
                        try {
                            if (anchorGroups_1_1 && !anchorGroups_1_1.done && (_a = anchorGroups_1.return)) _a.call(anchorGroups_1);
                        }
                        finally { if (e_2) throw e_2.error; }
                    }
                    map.forEach(function (anchors) {
                        var x1 = anchors[0][0].points[0].x;
                        var y1 = anchors[0][0].points[0].y;
                        var x2 = anchors[0][0].points[1].x;
                        var y2 = anchors[0][0].points[1].y;
                        var p1 = anchors[0][0].coordinateSystem.transformPoint(x1, y1);
                        var p2 = anchors[0][0].coordinateSystem.transformPoint(x2, y2);
                        var pd = Math.sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y));
                        var cx = (p1.x + p2.x) / 2;
                        var cy = (p1.y + p2.y) / 2;
                        var order = anchors.map(function (anchor) {
                            var p = anchor[1].coordinateSystem.transformPoint(anchor[1].points[0].x, anchor[1].points[0].y);
                            var proj = (p.x - cx) * (p2.x - p1.x) + (p.y - cy) * (p2.y - p1.y);
                            var distance = Math.sqrt((p.x - cx) * (p.x - cx) + (p.y - cy) * (p.y - cy));
                            var cosTheta = proj / distance / pd;
                            if (cosTheta > 0.999999) {
                                return 1 + distance;
                            }
                            else if (cosTheta < -0.999999) {
                                return -1 - distance;
                            }
                            return cosTheta;
                            // return proj;
                        });
                        var indices = [];
                        var totalWidth = 0;
                        for (var i = 0; i < anchors.length; i++) {
                            indices.push(i);
                            totalWidth += anchors[i][0].strokeWidth;
                        }
                        indices.sort(function (a, b) { return order[a] - order[b]; });
                        var cWidth = 0;
                        for (var i = 0; i < anchors.length; i++) {
                            var m = indices[i];
                            var k1 = cWidth / totalWidth;
                            cWidth += anchors[m][0].strokeWidth;
                            var k2 = cWidth / totalWidth;
                            anchors[m][0].points[0].x = x1 + (x2 - x1) * k1;
                            anchors[m][0].points[0].y = y1 + (y2 - y1) * k1;
                            anchors[m][0].points[1].x = x1 + (x2 - x1) * k2;
                            anchors[m][0].points[1].y = y1 + (y2 - y1) * k2;
                        }
                    });
                }
                return Graphics.makeGroup(anchorGroups.map(function (anchors) {
                    var bands = [];
                    for (var i = 0; i < anchors.length - 1; i++) {
                        var path = Graphics.makePath({
                            fillColor: anchors[i][0].color,
                            fillOpacity: anchors[i][0].opacity,
                        });
                        LinksClass.LinkPath(path, linkGraphics, lineType, anchors[i][0], anchors[i + 1][1]);
                        bands.push(path.path);
                    }
                    return Graphics.makeGroup(bands);
                }));
            }
        }
    };
    /** Get the graphics that represent this layout */
    // eslint-disable-next-line
    LinksClass.prototype.getGraphics = function (manager) {
        return null;
    };
    // eslint-disable-next-line max-lines-per-function
    LinksClass.prototype.getAttributePanelWidgets = function (manager) {
        var props = this.object.properties;
        var lineWidgets = [];
        var widgets = [];
        lineWidgets.push(manager.inputSelect({ property: "interpolationType" }, {
            type: "dropdown",
            showLabel: true,
            options: ["line", "bezier", "circle"],
            labels: [
                strings_1.strings.objects.links.line,
                strings_1.strings.objects.links.bezier,
                strings_1.strings.objects.links.arc,
            ],
            label: strings_1.strings.objects.links.type,
            searchSection: strings_1.strings.objects.general,
        }), props.linkType == "line"
            ? manager.inputSelect({ property: "linkMarkType" }, {
                type: "dropdown",
                showLabel: true,
                options: ["", "8", "1 10"],
                labels: [
                    strings_1.strings.objects.links.solid,
                    strings_1.strings.objects.links.dashed,
                    strings_1.strings.objects.links.dotted,
                ],
                label: strings_1.strings.objects.links.linkMarkType,
                icons: ["line", "stroke/dashed", "stroke/dotted"],
                isLocalIcons: true,
                searchSection: strings_1.strings.objects.general,
            })
            : null);
        if (props.linkType == "line") {
            lineWidgets.push(manager.inputSelect({ property: "beginArrowType" }, {
                type: "dropdown",
                showLabel: true,
                options: [
                    ArrowType.NO_ARROW,
                    ArrowType.ARROW,
                    ArrowType.DIAMOND_ARROW,
                    ArrowType.OVAL_ARROW,
                ],
                labels: [
                    strings_1.strings.objects.arrows.noArrow,
                    strings_1.strings.objects.arrows.arrow,
                    strings_1.strings.objects.arrows.diamondArrow,
                    strings_1.strings.objects.arrows.ovalArrow,
                ],
                label: strings_1.strings.objects.arrows.beginArrowType,
                icons: [
                    "noArrow",
                    "beginArrow",
                    "beginDiamondArrow",
                    "beginOvalArrow",
                ],
                isLocalIcons: true,
                searchSection: strings_1.strings.objects.general,
            }));
            lineWidgets.push(manager.inputSelect({ property: "endArrowType" }, {
                type: "dropdown",
                showLabel: true,
                options: [
                    ArrowType.NO_ARROW,
                    ArrowType.ARROW,
                    ArrowType.DIAMOND_ARROW,
                    ArrowType.OVAL_ARROW,
                ],
                labels: [
                    strings_1.strings.objects.arrows.noArrow,
                    strings_1.strings.objects.arrows.arrow,
                    strings_1.strings.objects.arrows.diamondArrow,
                    strings_1.strings.objects.arrows.ovalArrow,
                ],
                label: strings_1.strings.objects.arrows.endArrowType,
                icons: ["noArrow", "endArrow", "endDiamondArrow", "endOvalArrow"],
                isLocalIcons: true,
                searchSection: strings_1.strings.objects.general,
            }));
        }
        if (utils_1.shouldShowCloseLink(this.parent, props)) {
            lineWidgets.push(manager.inputBoolean({ property: "closeLink" }, {
                type: "checkbox",
                label: strings_1.strings.objects.links.closeLink,
                checkBoxStyles: {
                    root: {
                        marginTop: 5,
                    },
                },
                searchSection: strings_1.strings.objects.general,
            }));
        }
        if (props.interpolationType == "bezier") {
            lineWidgets.push(manager.inputNumber({ property: "curveness" }, {
                showSlider: true,
                minimum: 0,
                sliderRange: [0, 500],
                label: strings_1.strings.objects.links.curveness,
                searchSection: strings_1.strings.objects.general,
            }));
        }
        widgets.push(manager.verticalGroup({ header: strings_1.strings.objects.general }, lineWidgets));
        widgets.push(manager.verticalGroup({ header: strings_1.strings.objects.style }, [
            manager.mappingEditor(strings_1.strings.objects.color, "color", {
                table: props.linkTable && props.linkTable.table,
                acceptLinksTable: !!(props.linkTable && props.linkTable.table),
                searchSection: strings_1.strings.objects.style,
            }),
            manager.mappingEditor(strings_1.strings.objects.width, "strokeWidth", {
                hints: { rangeNumber: [0, 5] },
                defaultValue: 1,
                numberOptions: { showSlider: true, sliderRange: [0, 5], minimum: 0 },
                table: props.linkTable && props.linkTable.table,
                acceptLinksTable: !!(props.linkTable && props.linkTable.table),
                searchSection: strings_1.strings.objects.style,
            }),
            manager.mappingEditor(strings_1.strings.objects.opacity, "opacity", {
                hints: { rangeNumber: [0, 1] },
                defaultValue: 1,
                numberOptions: {
                    showSlider: true,
                    minimum: 0,
                    maximum: 1,
                    step: 0.1,
                },
                table: props.linkTable && props.linkTable.table,
                acceptLinksTable: !!(props.linkTable && props.linkTable.table),
                searchSection: strings_1.strings.objects.style,
            }),
        ]));
        return widgets;
    };
    LinksClass.prototype.getTemplateParameters = function () {
        var properties = [];
        if (this.object.mappings.color &&
            this.object.mappings.color.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "color",
                },
                type: Specification.AttributeType.Color,
                default: this.object.mappings.color &&
                    common_1.rgbToHex((this.object.mappings.color.value)),
            });
        }
        if (this.object.mappings.strokeWidth &&
            this.object.mappings.strokeWidth.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "strokeWidth",
                },
                type: Specification.AttributeType.Number,
                default: this.object.mappings.strokeWidth &&
                    (this.object.mappings.strokeWidth.value),
            });
        }
        if (this.object.mappings.opacity &&
            this.object.mappings.opacity.type === specification_1.MappingType.value) {
            properties.push({
                objectID: this.object._id,
                target: {
                    attribute: "opacity",
                },
                type: Specification.AttributeType.Number,
                default: this.object.mappings.opacity &&
                    (this.object.mappings.opacity.value),
            });
        }
        return {
            properties: properties,
        };
    };
    LinksClass.metadata = {
        iconPath: "CharticulatorLine",
    };
    return LinksClass;
}(chart_element_1.ChartElementClass));
exports.LinksClass = LinksClass;
var SeriesLinksClass = /** @class */ (function (_super) {
    __extends(SeriesLinksClass, _super);
    function SeriesLinksClass() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    /** Get the graphics that represent this layout */
    SeriesLinksClass.prototype.getGraphics = function (manager) {
        var _this = this;
        var props = this.object.properties;
        var linkGroup = Graphics.makeGroup([]);
        var renderState = {
            colorFunction: this.parent.resolveMapping(this.object.mappings.color, {
                r: 0,
                g: 0,
                b: 0,
            }),
            opacityFunction: this.parent.resolveMapping(this.object.mappings.opacity, 1),
            strokeWidthFunction: this.parent.resolveMapping(this.object.mappings.strokeWidth, 1),
        };
        var chart = this.parent.object;
        var chartState = this.parent.state;
        // Resolve the anchors
        var layoutIndex = common_1.indexOf(chart.elements, function (l) { return l._id == props.linkThrough.plotSegment; });
        var layout = chart.elements[layoutIndex];
        var mark = common_1.getById(chart.glyphs, layout.glyph);
        var layoutState = (chartState.elements[layoutIndex]);
        var layoutClass = manager.getPlotSegmentClass(layoutState);
        var table = this.parent.dataflow.getTable(layout.table);
        var facets = facetRows(table, layoutState.dataRowIndices, props.linkThrough.facetExpressions.map(function (x) {
            return _this.parent.dataflow.cache.parse(x);
        }));
        var rowToMarkState = new Map();
        for (var i = 0; i < layoutState.dataRowIndices.length; i++) {
            rowToMarkState.set(layoutState.dataRowIndices[i].join(","), layoutState.glyphs[i]);
        }
        var anchor1 = this.resolveLinkAnchorPoints(props.anchor1, mark);
        var anchor2 = this.resolveLinkAnchorPoints(props.anchor2, mark);
        var anchors = facets.map(function (facet) {
            return facet.map(function (index) {
                var markState = rowToMarkState.get(index.join(","));
                var row = table.getGroupedContext(index);
                if (markState) {
                    return [
                        _this.getAnchorPoints(renderState, anchor1, layoutClass, markState, row),
                        _this.getAnchorPoints(renderState, anchor2, layoutClass, markState, row),
                    ];
                }
                else {
                    return null;
                }
            });
        });
        try {
            if (utils_1.shouldShowCloseLink(this.parent, props, true)) {
                for (var i = 0; i < anchors.length; i++) {
                    var currentAnchor = anchors[i];
                    currentAnchor.push([
                        currentAnchor[currentAnchor.length - 1][1],
                        currentAnchor[0][0],
                    ]);
                }
            }
        }
        catch (e) {
            //error
        }
        linkGroup.elements.push(this.renderLinks(props.linkType, props.interpolationType, anchors, props.linkMarkType));
        return linkGroup;
    };
    SeriesLinksClass.classID = "links.through";
    SeriesLinksClass.type = "links";
    SeriesLinksClass.defaultProperties = {
        visible: true,
        closeLink: false,
        beginArrowType: ArrowType.NO_ARROW,
        endArrowType: ArrowType.NO_ARROW,
    };
    return SeriesLinksClass;
}(LinksClass));
exports.SeriesLinksClass = SeriesLinksClass;
var LayoutsLinksClass = /** @class */ (function (_super) {
    __extends(LayoutsLinksClass, _super);
    function LayoutsLinksClass() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    /** Get the graphics that represent this layout */
    LayoutsLinksClass.prototype.getGraphics = function (manager) {
        var props = this.object.properties;
        var linkGroup = Graphics.makeGroup([]);
        var renderState = {
            colorFunction: this.parent.resolveMapping(this.object.mappings.color, {
                r: 0,
                g: 0,
                b: 0,
            }),
            opacityFunction: this.parent.resolveMapping(this.object.mappings.opacity, 1),
            strokeWidthFunction: this.parent.resolveMapping(this.object.mappings.strokeWidth, 1),
        };
        var chart = this.parent.object;
        var chartState = this.parent.state;
        var layoutIndices = props.linkBetween.plotSegments.map(function (lid) {
            return common_1.indexOf(chart.elements, function (l) { return l._id == lid; });
        });
        var layouts = (layoutIndices.map(function (i) { return chart.elements[i]; }));
        var layoutStates = (layoutIndices.map(function (i) { return chartState.elements[i]; }));
        var layoutClasses = layoutStates.map(function (layoutState) {
            return manager.getPlotSegmentClass(layoutState);
        });
        var glyphs = layouts.map(function (layout) { return common_1.getById(chart.glyphs, layout.glyph); });
        var anchor1 = this.resolveLinkAnchorPoints(props.anchor1, glyphs[0]);
        var anchor2 = this.resolveLinkAnchorPoints(props.anchor2, glyphs[1]);
        for (var shift = 0; shift < layoutStates.length - 1; shift++) {
            var rowIndicesMap = new Map();
            for (var i = 0; i < layoutStates[shift].dataRowIndices.length; i++) {
                rowIndicesMap.set(layoutStates[shift].dataRowIndices[i].join(","), i);
            }
            var table = this.parent.dataflow.getTable(layouts[0].table);
            var anchors = [];
            for (var i1 = 0; i1 < layoutStates[shift + 1].dataRowIndices.length; i1++) {
                var rowIndex = layoutStates[shift + 1].dataRowIndices[i1];
                var rowIndexJoined = rowIndex.join(",");
                if (rowIndicesMap.has(rowIndexJoined)) {
                    var i0 = rowIndicesMap.get(rowIndexJoined);
                    var row = table.getGroupedContext(rowIndex);
                    anchors.push([
                        [
                            this.getAnchorPoints(renderState, anchor1, layoutClasses[shift], layoutStates[shift].glyphs[i0], row),
                            null,
                        ],
                        [
                            null,
                            this.getAnchorPoints(renderState, anchor2, layoutClasses[shift + 1], layoutStates[shift + 1].glyphs[i1], row),
                        ],
                    ]);
                }
            }
            linkGroup.elements.push(this.renderLinks(props.linkType, props.interpolationType, anchors, props.linkMarkType));
        }
        return linkGroup;
    };
    LayoutsLinksClass.classID = "links.between";
    LayoutsLinksClass.type = "links";
    LayoutsLinksClass.defaultProperties = {
        visible: true,
        closeLink: false,
        beginArrowType: ArrowType.NO_ARROW,
        endArrowType: ArrowType.NO_ARROW,
    };
    return LayoutsLinksClass;
}(LinksClass));
exports.LayoutsLinksClass = LayoutsLinksClass;
var TableLinksClass = /** @class */ (function (_super) {
    __extends(TableLinksClass, _super);
    function TableLinksClass() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    /** Get the graphics that represent this layout */
    // eslint-disable-next-line
    TableLinksClass.prototype.getGraphics = function (manager) {
        var _this = this;
        var props = this.object.properties;
        var linkGroup = Graphics.makeGroup([]);
        var renderState = {
            colorFunction: this.parent.resolveMapping(this.object.mappings.color, {
                r: 0,
                g: 0,
                b: 0,
            }),
            opacityFunction: this.parent.resolveMapping(this.object.mappings.opacity, 1),
            strokeWidthFunction: this.parent.resolveMapping(this.object.mappings.strokeWidth, 1),
        };
        var chart = this.parent.object;
        var chartState = this.parent.state;
        var layoutIndices = props.linkTable.plotSegments.map(function (lid) {
            return common_1.indexOf(chart.elements, function (l) { return l._id == lid; });
        });
        var layouts = (layoutIndices.map(function (i) { return chart.elements[i]; }));
        var layoutStates = (layoutIndices.map(function (i) { return chartState.elements[i]; }));
        var layoutClasses = layoutStates.map(function (layoutState) {
            return manager.getPlotSegmentClass(layoutState);
        });
        var glyphs = layouts.map(function (layout) { return common_1.getById(chart.glyphs, layout.glyph); });
        var anchor1 = this.resolveLinkAnchorPoints(props.anchor1, glyphs[0]);
        var anchor2 = this.resolveLinkAnchorPoints(props.anchor2, glyphs[1]);
        var linkTable = this.parent.dataflow.getTable(props.linkTable.table);
        var tables = layouts.map(function (layout, layoutIndex) {
            var table = _this.parent.dataflow.getTable(layout.table);
            var id2RowGlyphIndex = new Map();
            for (var i = 0; i < layoutStates[layoutIndex].dataRowIndices.length; i++) {
                var rowIndex = layoutStates[layoutIndex].dataRowIndices[i];
                var rowIDs = rowIndex.map(function (i) { return table.getRow(i).id; }).join(",");
                id2RowGlyphIndex.set(rowIDs, [rowIndex, i]);
            }
            return {
                table: table,
                id2RowGlyphIndex: id2RowGlyphIndex,
            };
        });
        // Prepare data rows
        var rowIndices = [];
        for (var i = 0; i < linkTable.rows.length; i++) {
            rowIndices.push(i);
        }
        var anchors = [];
        for (var i = 0; i < rowIndices.length; i++) {
            var rowIndex = rowIndices[i];
            var row = linkTable.getGroupedContext([rowIndex]);
            var rowItem = linkTable.getRow(rowIndex);
            var r1 = rowItem.source_id &&
                tables[0].id2RowGlyphIndex.get(rowItem.source_id.toString());
            var r2 = rowItem.target_id &&
                tables[1].id2RowGlyphIndex.get(rowItem.target_id.toString());
            if (!r1 || !r2) {
                continue;
            }
            // eslint-disable-next-line
            var _a = __read(r1, 2), iRow0 = _a[0], i0 = _a[1];
            // eslint-disable-next-line
            var _b = __read(r2, 2), iRow1 = _b[0], i1 = _b[1];
            anchors.push([
                [
                    this.getAnchorPoints(renderState, anchor1, layoutClasses[0], layoutStates[0].glyphs[i0], row),
                    null,
                ],
                [
                    null,
                    this.getAnchorPoints(renderState, anchor2, layoutClasses[1], layoutStates[1].glyphs[i1], row),
                ],
            ]);
        }
        linkGroup.elements.push(this.renderLinks(props.linkType, props.interpolationType, anchors, props.linkMarkType));
        return linkGroup;
    };
    TableLinksClass.classID = "links.table";
    TableLinksClass.type = "links";
    TableLinksClass.defaultProperties = {
        visible: true,
        beginArrowType: ArrowType.NO_ARROW,
        endArrowType: ArrowType.NO_ARROW,
    };
    return TableLinksClass;
}(LinksClass));
exports.TableLinksClass = TableLinksClass;
function registerClasses() {
    object_1.ObjectClasses.Register(SeriesLinksClass);
    object_1.ObjectClasses.Register(LayoutsLinksClass);
    object_1.ObjectClasses.Register(TableLinksClass);
}
exports.registerClasses = registerClasses;
//# sourceMappingURL=index.js.map