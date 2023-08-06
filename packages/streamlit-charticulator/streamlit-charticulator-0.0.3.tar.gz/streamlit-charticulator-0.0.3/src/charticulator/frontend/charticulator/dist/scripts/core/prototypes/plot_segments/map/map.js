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
var __spread = (this && this.__spread) || function () {
    for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
    return ar;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.MapPlotSegment = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var Graphics = require("../../../graphics");
var solver_1 = require("../../../solver");
var Specification = require("../../../specification");
var common_1 = require("../../../common");
var plot_segment_1 = require("../plot_segment");
var axis_1 = require("../axis");
var map_service_1 = require("./map_service");
var MapPlotSegment = /** @class */ (function (_super) {
    __extends(MapPlotSegment, _super);
    function MapPlotSegment() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.attributeNames = ["x1", "x2", "y1", "y2"];
        _this.attributes = {
            x1: {
                name: "x1",
                type: Specification.AttributeType.Number,
            },
            x2: {
                name: "x2",
                type: Specification.AttributeType.Number,
            },
            y1: {
                name: "y1",
                type: Specification.AttributeType.Number,
            },
            y2: {
                name: "y2",
                type: Specification.AttributeType.Number,
            },
        };
        // The map service for this map
        _this.mapService = map_service_1.StaticMapService.GetService();
        return _this;
    }
    MapPlotSegment.prototype.initializeState = function () {
        var attrs = this.state.attributes;
        attrs.x1 = -100;
        attrs.x2 = 100;
        attrs.y1 = -100;
        attrs.y2 = 100;
    };
    MapPlotSegment.prototype.buildGlyphConstraints = function (solver) {
        var e_1, _a;
        // const [latitude, longitude, zoom] = this.getCenterZoom();
        var longitudeData = this.object.properties.longitudeData;
        var latitudeData = this.object.properties.latitudeData;
        if (latitudeData && longitudeData) {
            var latExpr = this.parent.dataflow.cache.parse(latitudeData.expression);
            var lngExpr = this.parent.dataflow.cache.parse(longitudeData.expression);
            var table = this.parent.dataflow.getTable(this.object.table);
            try {
                for (var _b = __values(common_1.zipArray(this.state.glyphs, this.state.dataRowIndices)), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var _d = __read(_c.value, 2), glyphState = _d[0], index = _d[1];
                    var row = table.getGroupedContext(index);
                    var lat = latExpr.getNumberValue(row);
                    var lng = lngExpr.getNumberValue(row);
                    var p = this.getProjectedPoints([[lat, lng]])[0];
                    solver.addLinear(solver_1.ConstraintStrength.HARD, p[0], [], [[1, solver.attr(glyphState.attributes, "x")]]);
                    solver.addLinear(solver_1.ConstraintStrength.HARD, p[1], [], [[1, solver.attr(glyphState.attributes, "y")]]);
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
    };
    MapPlotSegment.prototype.getBoundingBox = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, x2 = attrs.x2, y1 = attrs.y1, y2 = attrs.y2;
        return {
            type: "rectangle",
            cx: (x1 + x2) / 2,
            cy: (y1 + y2) / 2,
            width: Math.abs(x2 - x1),
            height: Math.abs(y2 - y1),
            rotation: 0,
        };
    };
    MapPlotSegment.prototype.getSnappingGuides = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        return [
            { type: "x", value: x1, attribute: "x1" },
            { type: "x", value: x2, attribute: "x2" },
            { type: "y", value: y1, attribute: "y1" },
            { type: "y", value: y2, attribute: "y2" },
        ];
    };
    MapPlotSegment.prototype.mercatorProjection = function (lat, lng) {
        // WebMercator Projection:
        // x, y range: [0, 256]
        var x = (128 / 180) * (180 + lng);
        var y = (128 / 180) *
            (180 -
                (180 / Math.PI) *
                    Math.log(Math.tan(Math.PI / 4 + common_1.Geometry.degreesToRadians(lat) / 2)));
        return [x, y];
        // // Bing's version as of here: https://msdn.microsoft.com/en-us/library/bb259689.aspx
        // // Same as Google's Version
        // let sin = Math.sin(lat / 180 * Math.PI);
        // let x1 = (lng + 180) / 360 * 256;
        // let y1 = (0.5 - Math.log((1 + sin) / (1 - sin)) / (4 * Math.PI)) * 256;
        // console.log((x - x1).toFixed(8), (y - y1).toFixed(8));
    };
    // Get (x, y) coordinates based on longitude and latitude
    MapPlotSegment.prototype.getProjectedPoints = function (points) {
        var _this = this;
        var attrs = this.state.attributes;
        var _a = __read(this.getCenterZoom(), 3), cLatitude = _a[0], cLongitude = _a[1], zoom = _a[2];
        var _b = __read(this.mercatorProjection(cLatitude, cLongitude), 2), cX = _b[0], cY = _b[1];
        var scale = Math.pow(2, zoom);
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        return points.map(function (p) {
            var _a = __read(_this.mercatorProjection(p[0], p[1]), 2), x = _a[0], y = _a[1];
            return [
                (x - cX) * scale + (x1 + x2) / 2,
                -(y - cY) * scale + (y1 + y2) / 2,
            ];
        });
    };
    MapPlotSegment.prototype.getCenterZoom = function () {
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var minLongitude = -180;
        var maxLongitude = 180;
        var minLatitude = -50;
        var maxLatitude = 50;
        if (props.latitudeData != null) {
            minLatitude = props.latitudeData.domainMin;
            maxLatitude = props.latitudeData.domainMax;
        }
        if (props.longitudeData != null) {
            minLongitude = props.longitudeData.domainMin;
            maxLongitude = props.longitudeData.domainMax;
        }
        var _a = __read(this.mercatorProjection(minLatitude, minLongitude), 2), xMin = _a[0], yMin = _a[1];
        var _b = __read(this.mercatorProjection(maxLatitude, maxLongitude), 2), xMax = _b[0], yMax = _b[1];
        // Find the appropriate zoom level for the given box.
        var scaleX = Math.abs(Math.abs(attrs.x2 - attrs.x1) / Math.abs(xMax - xMin));
        var scaleY = Math.abs(Math.abs(attrs.y2 - attrs.y1) / Math.abs(yMax - yMin));
        var scale = Math.min(scaleX, scaleY);
        var zoom = Math.floor(Math.log2(scale));
        var latitude = (minLatitude + maxLatitude) / 2;
        var longitude = (minLongitude + maxLongitude) / 2;
        return [latitude, longitude, zoom];
    };
    MapPlotSegment.prototype.getPlotSegmentGraphics = function (glyphGraphics) {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        var _a = __read(this.getCenterZoom(), 3), latitude = _a[0], longitude = _a[1], zoom = _a[2];
        var width = x2 - x1;
        var height = y2 - y1;
        var img = {
            type: "image",
            src: this.mapService.getImageryURLAtPoint({
                center: {
                    latitude: latitude,
                    longitude: longitude,
                },
                type: this.object.properties.mapType,
                zoom: zoom,
                width: width,
                height: height,
                resolution: "high",
            }),
            x: x1,
            y: y1,
            width: width,
            height: height,
        };
        return Graphics.makeGroup([img, glyphGraphics]);
    };
    MapPlotSegment.prototype.getDropZones = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        var zones = [];
        zones.push({
            type: "line",
            p1: { x: x2, y: y1 },
            p2: { x: x1, y: y1 },
            title: "Longitude",
            dropAction: {
                axisInference: { property: "longitudeData" },
            },
        });
        zones.push({
            type: "line",
            p1: { x: x1, y: y1 },
            p2: { x: x1, y: y2 },
            title: "Latitude",
            dropAction: {
                axisInference: { property: "latitudeData" },
            },
        });
        return zones;
    };
    MapPlotSegment.prototype.getHandles = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, x2 = attrs.x2, y1 = attrs.y1, y2 = attrs.y2;
        var h = [
            {
                type: "line",
                axis: "y",
                value: y1,
                span: [x1, x2],
                actions: [{ type: "attribute", attribute: "y1" }],
            },
            {
                type: "line",
                axis: "y",
                value: y2,
                span: [x1, x2],
                actions: [{ type: "attribute", attribute: "y2" }],
            },
            {
                type: "line",
                axis: "x",
                value: x1,
                span: [y1, y2],
                actions: [{ type: "attribute", attribute: "x1" }],
            },
            {
                type: "line",
                axis: "x",
                value: x2,
                span: [y1, y2],
                actions: [{ type: "attribute", attribute: "x2" }],
            },
            {
                type: "point",
                x: x1,
                y: y1,
                actions: [
                    { type: "attribute", source: "x", attribute: "x1" },
                    { type: "attribute", source: "y", attribute: "y1" },
                ],
            },
            {
                type: "point",
                x: x2,
                y: y1,
                actions: [
                    { type: "attribute", source: "x", attribute: "x2" },
                    { type: "attribute", source: "y", attribute: "y1" },
                ],
            },
            {
                type: "point",
                x: x1,
                y: y2,
                actions: [
                    { type: "attribute", source: "x", attribute: "x1" },
                    { type: "attribute", source: "y", attribute: "y2" },
                ],
            },
            {
                type: "point",
                x: x2,
                y: y2,
                actions: [
                    { type: "attribute", source: "x", attribute: "x2" },
                    { type: "attribute", source: "y", attribute: "y2" },
                ],
            },
        ];
        return h;
    };
    MapPlotSegment.prototype.getAttributePanelWidgets = function (m) {
        var props = this.object.properties;
        var widgets = __spread(axis_1.buildAxisWidgets(props.latitudeData, "latitudeData", m, "Latitude"), axis_1.buildAxisWidgets(props.longitudeData, "longitudeData", m, "Longitude"), [
            m.sectionHeader("Map Style"),
            m.inputSelect({ property: "mapType" }, {
                type: "dropdown",
                showLabel: true,
                labels: ["Roadmap", "Satellite", "Hybrid", "Terrain"],
                options: ["roadmap", "satellite", "hybrid", "terrain"],
            }),
        ]);
        return widgets;
    };
    MapPlotSegment.classID = "plot-segment.map";
    MapPlotSegment.type = "plot-segment";
    MapPlotSegment.metadata = {
        iconPath: "plot-segment/map",
    };
    MapPlotSegment.defaultMappingValues = {};
    MapPlotSegment.defaultProperties = {
        mapType: "roadmap",
    };
    return MapPlotSegment;
}(plot_segment_1.PlotSegmentClass));
exports.MapPlotSegment = MapPlotSegment;
//# sourceMappingURL=map.js.map