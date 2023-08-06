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
exports.EditingLink = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var Hammer = require("hammerjs");
var React = require("react");
var core_1 = require("../../../core");
var actions_1 = require("../../actions");
var renderer_1 = require("../../renderer");
var EditingLink = /** @class */ (function (_super) {
    __extends(EditingLink, _super);
    function EditingLink(props) {
        var _this = _super.call(this, props) || this;
        _this.markPlaceholders = new WeakMap();
        _this.state = {
            stage: "select-source",
            firstAnchor: null,
            secondAnchor: null,
            currentMouseLocation: { x: 0, y: 0 },
        };
        return _this;
    }
    EditingLink.prototype.getMarkAtPoint = function (x, y) {
        var element = document.elementFromPoint(x, y);
        var mark = null;
        while (element) {
            if (element instanceof SVGGElement) {
                if (this.markPlaceholders.has(element)) {
                    mark = this.markPlaceholders.get(element);
                    break;
                }
            }
            element = element.parentElement;
        }
        return mark;
    };
    EditingLink.prototype.componentDidMount = function () {
        var _this = this;
        this.hammer = new Hammer(this.refs.container);
        this.hammer.add(new Hammer.Pan());
        this.hammer.add(new Hammer.Tap());
        this.hammer.on("tap panend", function (e) {
            var pageX = e.center.x;
            var pageY = e.center.y;
            var markInfo = _this.getMarkAtPoint(pageX, pageY);
            if (markInfo) {
                var anchor = markInfo.anchor.points.map(function (pt) {
                    return {
                        x: { element: markInfo.anchor.element, attribute: pt.xAttribute },
                        y: { element: markInfo.anchor.element, attribute: pt.yAttribute },
                        direction: pt.direction,
                    };
                });
                if (markInfo.mode == "begin") {
                    new actions_1.Actions.SetObjectProperty(_this.props.link, "anchor1", null, anchor).dispatch(_this.props.store.dispatcher);
                }
                else {
                    new actions_1.Actions.SetObjectProperty(_this.props.link, "anchor2", null, anchor).dispatch(_this.props.store.dispatcher);
                }
            }
            else {
                new actions_1.Actions.ClearSelection().dispatch(_this.props.store.dispatcher);
            }
        });
    };
    EditingLink.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
    };
    EditingLink.prototype.renderAnchor = function (coordinateSystem, dx, dy, anchor) {
        var _this = this;
        var transformPoint = function (point) {
            var x = point.x + dx;
            var y = point.y + dy;
            var p = coordinateSystem.transformPoint(x, y);
            p = core_1.Graphics.transform(coordinateSystem.getBaseTransform(), p);
            return core_1.Geometry.applyZoom(_this.props.zoom, { x: p.x, y: -p.y });
        };
        if (anchor.points.length == 2) {
            var path = core_1.Graphics.makePath();
            core_1.Prototypes.Links.LinksClass.BandPath(path, {
                points: anchor.points.map(function (p) {
                    return { x: p.x + dx, y: p.y + dy, direction: p.direction };
                }),
                coordinateSystem: coordinateSystem,
                curveness: this.props.link.properties.curveness,
            }, false, true);
            var transform = "translate(" + this.props.zoom.centerX + "," + this.props.zoom.centerY + ") scale(" + this.props.zoom.scale + ")";
            var d = renderer_1.renderSVGPath(path.path.cmds);
            return (React.createElement("g", { transform: transform },
                React.createElement("path", { d: d, className: "element-ghost-stroke", vectorEffect: "non-scaling-stroke" }),
                React.createElement("path", { d: d, className: "element-stroke", vectorEffect: "non-scaling-stroke" })));
            // let p1 = transformPoint(anchor.points[0]);
            // let p2 = transformPoint(anchor.points[1]);
            // return (
            //     <g>
            //         <line className="element-ghost-stroke" x1={p1.x} y1={p1.y} x2={p2.x} y2={p2.y} />
            //         <line className="element-stroke" x1={p1.x} y1={p1.y} x2={p2.x} y2={p2.y} />
            //     </g>
            // );
        }
        else {
            var p = transformPoint(anchor.points[0]);
            return (React.createElement("g", null,
                React.createElement("circle", { className: "element-ghost-shape", cx: p.x, cy: p.y, r: 8 }),
                React.createElement("circle", { className: "element-shape", cx: p.x, cy: p.y, r: 3 })));
        }
    };
    // eslint-disable-next-line
    EditingLink.prototype.renderMarkPlaceholders = function () {
        var _this = this;
        var _a, _b;
        var manager = this.props.store.chartManager;
        // Get the two glyphs
        var props = this.props.link
            .properties;
        var lineMode = props.linkType;
        var glyphs = [];
        switch (this.props.link.classID) {
            case "links.through":
                {
                    var plotSegmentClass = manager.getClassById(props.linkThrough.plotSegment);
                    var coordinateSystem = plotSegmentClass.getCoordinateSystem();
                    var facets = core_1.Prototypes.Links.facetRows(manager.dataflow.getTable(plotSegmentClass.object.table), plotSegmentClass.state.dataRowIndices, props.linkThrough.facetExpressions.map(function (x) {
                        return manager.dataflow.cache.parse(x);
                    }));
                    var glyph = core_1.getById(manager.chart.glyphs, plotSegmentClass.object.glyph);
                    var rowToMarkState = new Map();
                    for (var i = 0; i < plotSegmentClass.state.dataRowIndices.length; i++) {
                        rowToMarkState.set(plotSegmentClass.state.dataRowIndices[i].join(","), plotSegmentClass.state.glyphs[i]);
                    }
                    var firstNonEmptyFacet = 0;
                    for (; firstNonEmptyFacet < facets.length; firstNonEmptyFacet++) {
                        if (facets[firstNonEmptyFacet].length >= 2) {
                            break;
                        }
                    }
                    if (firstNonEmptyFacet < facets.length) {
                        glyphs = [
                            {
                                glyph: glyph,
                                glyphState: rowToMarkState.get(facets[firstNonEmptyFacet][0].join(",")),
                                coordinateSystem: coordinateSystem,
                            },
                            {
                                glyph: glyph,
                                glyphState: rowToMarkState.get(facets[firstNonEmptyFacet][1].join(",")),
                                coordinateSystem: coordinateSystem,
                            },
                        ];
                    }
                }
                break;
            case "links.between":
                {
                    var plotSegmentClasses = props.linkBetween.plotSegments.map(function (x) {
                        return manager.getClassById(x);
                    });
                    var glyphObjects = plotSegmentClasses.map(function (x) {
                        return core_1.getById(manager.chart.glyphs, x.object.glyph);
                    });
                    glyphs = [
                        {
                            glyph: glyphObjects[0],
                            glyphState: plotSegmentClasses[0].state.glyphs[0],
                            coordinateSystem: plotSegmentClasses[0].getCoordinateSystem(),
                        },
                        {
                            glyph: glyphObjects[1],
                            glyphState: plotSegmentClasses[1].state.glyphs[0],
                            coordinateSystem: plotSegmentClasses[1].getCoordinateSystem(),
                        },
                    ];
                }
                break;
            case "links.table":
                {
                    var plotSegmentClasses = props.linkTable.plotSegments.map(function (x) {
                        return manager.getClassById(x);
                    });
                    var glyphObjects = plotSegmentClasses.map(function (x) {
                        return core_1.getById(manager.chart.glyphs, x.object.glyph);
                    });
                    var linkTable = this.props.store.chartManager.dataflow.getTable(props.linkTable.table);
                    var tables_1 = plotSegmentClasses.map(function (plotSegmentClass) {
                        var table = _this.props.store.chartManager.dataflow.getTable(plotSegmentClass.object.table);
                        var id2RowGlyphIndex = new Map();
                        for (var i = 0; i < plotSegmentClass.state.dataRowIndices.length; i++) {
                            var rowIndex = plotSegmentClass.state.dataRowIndices[i];
                            var rowIDs = rowIndex.map(function (i) { return table.getRow(i).id; }).join(",");
                            id2RowGlyphIndex.set(rowIDs, [rowIndex, i]);
                        }
                        return {
                            table: table,
                            id2RowGlyphIndex: id2RowGlyphIndex,
                        };
                    });
                    // Find the first links with nodes are exists in main table
                    var rowItem = linkTable.rows.find(function (row) {
                        return row.source_id &&
                            tables_1[0].id2RowGlyphIndex.get(row.source_id.toString()) !=
                                undefined &&
                            row.target_id &&
                            tables_1[1].id2RowGlyphIndex.get(row.target_id.toString()) !=
                                undefined;
                    });
                    if (rowItem) {
                        var _c = __read(tables_1[0].id2RowGlyphIndex.get((_a = rowItem.source_id) === null || _a === void 0 ? void 0 : _a.toString()), 2), i0 = _c[1];
                        var _d = __read(tables_1[1].id2RowGlyphIndex.get((_b = rowItem.target_id) === null || _b === void 0 ? void 0 : _b.toString()), 2), i1 = _d[1];
                        glyphs = [
                            {
                                glyph: glyphObjects[0],
                                glyphState: plotSegmentClasses[0].state.glyphs[i0],
                                coordinateSystem: plotSegmentClasses[0].getCoordinateSystem(),
                            },
                            {
                                glyph: glyphObjects[1],
                                glyphState: plotSegmentClasses[1].state.glyphs[i1],
                                coordinateSystem: plotSegmentClasses[1].getCoordinateSystem(),
                            },
                        ];
                    }
                    else {
                        glyphs = [];
                    }
                }
                break;
        }
        // Render mark anchor candidates
        var elements = glyphs.map(function (_a, glyphIndex) {
            var glyph = _a.glyph, glyphState = _a.glyphState, coordinateSystem = _a.coordinateSystem;
            var anchorX = glyphState.marks[0].attributes.x;
            var anchorY = glyphState.marks[0].attributes.y;
            var offsetX = glyphState.attributes.x - anchorX;
            var offsetY = glyphState.attributes.y - anchorY;
            var marks = glyph.marks.map(function (element, elementIndex) {
                if (glyph.marks.length > 1 && element.classID == "mark.anchor") {
                    return null;
                }
                var markClass = manager.getMarkClass(glyphState.marks[elementIndex]);
                var mode = glyphIndex == 0 ? "begin" : "end";
                var anchors = markClass.getLinkAnchors
                    ? markClass.getLinkAnchors(mode)
                    : [];
                anchors = anchors.filter(function (anchor) {
                    if (lineMode == "line") {
                        return anchor.points.length == 1;
                    }
                    if (lineMode == "band") {
                        return anchor.points.length == 2;
                    }
                });
                return (React.createElement("g", { key: element._id }, anchors.map(function (anchor, index) { return (React.createElement("g", { className: "anchor", key: "m" + index, ref: function (g) {
                        if (g != null) {
                            _this.markPlaceholders.set(g, {
                                mode: mode,
                                markID: element._id,
                                anchor: anchor,
                                offsetX: offsetX,
                                offsetY: offsetY,
                                coordinateSystem: coordinateSystem,
                            });
                        }
                    } }, _this.renderAnchor(coordinateSystem, offsetX, offsetY, anchor))); })));
            });
            return React.createElement("g", { key: glyphIndex }, marks);
        });
        var currentAnchors = glyphs
            .map(function (_a, glyphIndex) {
            var glyph = _a.glyph, glyphState = _a.glyphState, coordinateSystem = _a.coordinateSystem;
            var anchorX = glyphState.marks[0].attributes.x;
            var anchorY = glyphState.marks[0].attributes.y;
            var offsetX = glyphState.attributes.x - anchorX;
            var offsetY = glyphState.attributes.y - anchorY;
            var anchor = glyphIndex == 0 ? props.anchor1 : props.anchor2;
            var element = anchor[0].x.element;
            if (!element) {
                return null;
            }
            var elementState = glyphState.marks[core_1.getIndexById(glyph.marks, element)];
            var anchorDescription = {
                element: element,
                points: anchor.map(function (a) {
                    return {
                        x: elementState.attributes[a.x.attribute],
                        xAttribute: a.x.attribute,
                        y: elementState.attributes[a.y.attribute],
                        yAttribute: a.y.attribute,
                        direction: a.direction,
                    };
                }),
            };
            return {
                coordinateSystem: coordinateSystem,
                offsetX: offsetX,
                offsetY: offsetY,
                anchor: anchorDescription,
            };
        })
            .filter(function (anchor) { return anchor != null; });
        var currentLinkElement = null;
        if (currentAnchors.length == 2) {
            var path = core_1.Graphics.makePath();
            var anchor1 = {
                coordinateSystem: currentAnchors[0].coordinateSystem,
                points: currentAnchors[0].anchor.points.map(function (p) {
                    return {
                        x: p.x + currentAnchors[0].offsetX,
                        y: p.y + currentAnchors[0].offsetY,
                        direction: p.direction,
                    };
                }),
                curveness: this.props.link.properties.curveness,
            };
            var anchor2 = {
                coordinateSystem: currentAnchors[1].coordinateSystem,
                points: currentAnchors[1].anchor.points.map(function (p) {
                    return {
                        x: p.x + currentAnchors[1].offsetX,
                        y: p.y + currentAnchors[1].offsetY,
                        direction: p.direction,
                    };
                }),
                curveness: this.props.link.properties.curveness,
            };
            core_1.Prototypes.Links.LinksClass.LinkPath(path, props.linkType, props.interpolationType, anchor1, anchor2);
            var transform = "translate(" + this.props.zoom.centerX + "," + this.props.zoom.centerY + ") scale(" + this.props.zoom.scale + ")";
            currentLinkElement = (React.createElement("g", { transform: transform },
                React.createElement("path", { d: renderer_1.renderSVGPath(path.path.cmds), className: "link-hint-" + props.linkType })));
        }
        return (React.createElement("g", null,
            currentLinkElement,
            elements,
            currentAnchors.map(function (_a, index) {
                var coordinateSystem = _a.coordinateSystem, offsetX = _a.offsetX, offsetY = _a.offsetY, anchor = _a.anchor;
                return (React.createElement("g", { className: "anchor active", key: index }, _this.renderAnchor(coordinateSystem, offsetX, offsetY, anchor)));
            })));
    };
    EditingLink.prototype.getPointFromEvent = function (point) {
        var r = this.refs.handler.getBoundingClientRect();
        var p = core_1.Geometry.unapplyZoom(this.props.zoom, {
            x: point.x - r.left,
            y: point.y - r.top,
        });
        return { x: p.x, y: -p.y };
    };
    EditingLink.prototype.render = function () {
        return (React.createElement("g", { className: "creating-link", ref: "container" }, this.renderMarkPlaceholders()));
    };
    return EditingLink;
}(React.Component));
exports.EditingLink = EditingLink;
//# sourceMappingURL=editing_link.js.map