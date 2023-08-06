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
exports.CreatingComponentFromCreatingInteraction = exports.CreatingComponent = exports.PointSnapping = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var Hammer = require("hammerjs");
var core_1 = require("../../../core");
var specification_1 = require("../../../core/specification");
var PointSnapping = /** @class */ (function () {
    function PointSnapping(guides, threshold) {
        if (threshold === void 0) { threshold = 10; }
        this.guides = guides;
        this.snappedGuides = new Set();
        this.threshold = threshold;
    }
    PointSnapping.prototype.beginSnapping = function () {
        this.snappedGuides = new Set();
    };
    PointSnapping.prototype.snapXValue = function (x) {
        var e_1, _a;
        var candidate = null;
        var candidateGuide = null;
        var candidateDistance = 1e10;
        var candidateValue = 0;
        try {
            for (var _b = __values(this.guides), _c = _b.next(); !_c.done; _c = _b.next()) {
                var guide = _c.value;
                switch (guide.guide.type) {
                    case "x":
                        {
                            var axis = guide.guide;
                            var d = Math.abs(axis.value - x);
                            if (d < this.threshold &&
                                (candidate == null || d < candidateDistance)) {
                                candidateDistance = d;
                                if (guide.element == null) {
                                    var parentMapping = {
                                        type: specification_1.MappingType.parent,
                                        parentAttribute: axis.attribute,
                                    };
                                    candidate = parentMapping;
                                }
                                else {
                                    var elementMapping = {
                                        type: specification_1.MappingType._element,
                                        element: guide.element._id,
                                        attribute: axis.attribute,
                                    };
                                    candidate = elementMapping;
                                }
                                candidateValue = axis.value;
                                candidateGuide = guide;
                            }
                        }
                        break;
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
        if (candidate) {
            this.snappedGuides.add(candidateGuide);
            return [candidateValue, candidate];
        }
        else {
            return [x, null];
        }
    };
    PointSnapping.prototype.snapYValue = function (y) {
        var e_2, _a;
        var candidate = null;
        var candidateGuide = null;
        var candidateDistance = 1e10;
        var candidateValue = 0;
        try {
            for (var _b = __values(this.guides), _c = _b.next(); !_c.done; _c = _b.next()) {
                var guide = _c.value;
                switch (guide.guide.type) {
                    case "y":
                        {
                            var axis = guide.guide;
                            var d = Math.abs(axis.value - y);
                            if (d < this.threshold &&
                                (candidate == null || d < candidateDistance)) {
                                candidateDistance = d;
                                if (guide.element == null) {
                                    var parentMapping = {
                                        type: specification_1.MappingType.parent,
                                        parentAttribute: axis.attribute,
                                    };
                                    candidate = parentMapping;
                                }
                                else {
                                    var elementMapping = {
                                        type: specification_1.MappingType._element,
                                        element: guide.element._id,
                                        attribute: axis.attribute,
                                    };
                                    candidate = elementMapping;
                                }
                                candidateValue = axis.value;
                                candidateGuide = guide;
                            }
                        }
                        break;
                }
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_2) throw e_2.error; }
        }
        if (candidate) {
            this.snappedGuides.add(candidateGuide);
            return [candidateValue, candidate];
        }
        else {
            return [y, null];
        }
    };
    PointSnapping.prototype.endSnapping = function () {
        return this.snappedGuides;
    };
    return PointSnapping;
}());
exports.PointSnapping = PointSnapping;
var CreatingComponent = /** @class */ (function (_super) {
    __extends(CreatingComponent, _super);
    function CreatingComponent(props) {
        var _this = _super.call(this, props) || this;
        _this.isHammering = false;
        _this.mode = _this.props.mode;
        _this.state = {
            points: null,
            draggingPoint: null,
            activeGuides: [],
            hoverCandidateX: null,
            hoverCandidateY: null,
        };
        return _this;
    }
    CreatingComponent.prototype.getPointFromEvent = function (point) {
        var r = this.refs.handler.getBoundingClientRect();
        var p = core_1.Geometry.unapplyZoom(this.props.zoom, {
            x: point.x - r.left,
            y: point.y - r.top,
        });
        return { x: p.x, y: -p.y };
    };
    CreatingComponent.prototype.initHammer = function () {
        var _this = this;
        this.hammer.remove("tap");
        this.hammer.remove("pan");
        switch (this.props.mode) {
            case "point":
            case "hline":
            case "vline":
                {
                    this.hammer.add(new Hammer.Tap());
                    this.hammer.on("tap", function (e) {
                        var p = _this.getPointFromEvent(e.center);
                        var p0X = _this.state.hoverCandidateX;
                        var p0Y = _this.state.hoverCandidateY;
                        if (p0X == null) {
                            p0X = [p.x, null];
                        }
                        if (p0Y == null) {
                            p0Y = [p.y, null];
                        }
                        if (_this.props.mode == "point") {
                            _this.props.onCreate(p0X, p0Y);
                        }
                        if (_this.props.mode == "hline") {
                            _this.props.onCreate(p0Y);
                        }
                        if (_this.props.mode == "vline") {
                            _this.props.onCreate(p0X);
                        }
                    });
                }
                break;
            case "line":
            case "rectangle": {
                this.hammer.add(new Hammer.Pan());
                this.hammer.add(new Hammer.Tap());
                this.hammer.on("tap", function () {
                    _this.props.onCancel();
                });
                var p0X_1 = null;
                var p0Y_1 = null;
                var p1X_1 = null;
                var p1Y_1 = null;
                this.hammer.on("panstart", function (e) {
                    _this.isHammering = true;
                    var p0 = _this.getPointFromEvent(core_1.Geometry.vectorSub(e.center, { x: e.deltaX, y: e.deltaY }));
                    var mgr = new PointSnapping(_this.props.guides, 10 / _this.props.zoom.scale);
                    mgr.beginSnapping();
                    p0X_1 = mgr.snapXValue(p0.x);
                    p0Y_1 = mgr.snapYValue(p0.y);
                    mgr.endSnapping();
                    _this.setState({
                        points: [{ x: p0X_1[0], y: p0Y_1[0] }],
                        draggingPoint: { x: p0X_1[0], y: p0Y_1[0] },
                    });
                });
                this.hammer.on("pan", function (e) {
                    var p1 = _this.getPointFromEvent(e.center);
                    var mgr = new PointSnapping(_this.props.guides, 10 / _this.props.zoom.scale);
                    mgr.beginSnapping();
                    p1X_1 = mgr.snapXValue(p1.x);
                    p1Y_1 = mgr.snapYValue(p1.y);
                    var guides = mgr.endSnapping();
                    _this.setState({
                        points: [{ x: p0X_1[0], y: p0Y_1[0] }],
                        draggingPoint: { x: p1X_1[0], y: p1Y_1[0] },
                        activeGuides: Array.from(guides),
                    });
                });
                this.hammer.on("panend", function () {
                    _this.isHammering = false;
                    _this.setState({
                        points: null,
                        draggingPoint: null,
                        activeGuides: [],
                    });
                    _this.props.onCreate(p0X_1, p0Y_1, p1X_1, p1Y_1);
                });
            }
        }
    };
    CreatingComponent.prototype.componentDidUpdate = function () {
        var _a;
        if (this.mode !== this.props.mode) {
            this.mode = this.props.mode;
            (_a = this.hammer) === null || _a === void 0 ? void 0 : _a.destroy();
            this.hammer = new Hammer(this.refs.handler);
            this.initHammer();
        }
    };
    CreatingComponent.prototype.componentDidMount = function () {
        this.hammer = new Hammer(this.refs.handler);
        this.initHammer();
    };
    CreatingComponent.prototype.componentWillUnmount = function () {
        this.hammer.destroy();
    };
    CreatingComponent.prototype.getPixelPoint = function (p) {
        return core_1.Geometry.applyZoom(this.props.zoom, { x: p.x, y: -p.y });
    };
    CreatingComponent.prototype.renderHint = function () {
        switch (this.props.mode) {
            case "point": {
                if (this.state.hoverCandidateX == null ||
                    this.state.hoverCandidateY == null) {
                    return null;
                }
                var pp = this.getPixelPoint({
                    x: this.state.hoverCandidateX[0],
                    y: this.state.hoverCandidateY[0],
                });
                return React.createElement("circle", { cx: pp.x, cy: pp.y, r: 3 });
            }
            case "hline": {
                if (this.state.hoverCandidateX == null ||
                    this.state.hoverCandidateY == null) {
                    return null;
                }
                var pp = this.getPixelPoint({
                    x: this.state.hoverCandidateX[0],
                    y: this.state.hoverCandidateY[0],
                });
                return React.createElement("line", { x1: 0, x2: this.props.width, y1: pp.y, y2: pp.y });
            }
            case "vline": {
                if (this.state.hoverCandidateX == null ||
                    this.state.hoverCandidateY == null) {
                    return null;
                }
                var pp = this.getPixelPoint({
                    x: this.state.hoverCandidateX[0],
                    y: this.state.hoverCandidateY[0],
                });
                return React.createElement("line", { y1: 0, y2: this.props.height, x1: pp.x, x2: pp.x });
            }
            case "line": {
                var _a = this.state, points = _a.points, draggingPoint = _a.draggingPoint;
                if (points == null || points.length != 1 || draggingPoint == null) {
                    return null;
                }
                var p1 = this.getPixelPoint(points[0]);
                var p2 = this.getPixelPoint(draggingPoint);
                return React.createElement("line", { x1: p1.x, y1: p1.y, x2: p2.x, y2: p2.y });
            }
            case "rectangle": {
                var _b = this.state, points = _b.points, draggingPoint = _b.draggingPoint;
                if (points == null || points.length != 1 || draggingPoint == null) {
                    return null;
                }
                var p1 = this.getPixelPoint(points[0]);
                var p2 = this.getPixelPoint(draggingPoint);
                return (React.createElement("rect", { x: Math.min(p1.x, p2.x), y: Math.min(p1.y, p2.y), width: Math.abs(p1.x - p2.x), height: Math.abs(p1.y - p2.y) }));
            }
        }
    };
    CreatingComponent.prototype.renderSnappingGuides = function () {
        var _this = this;
        var guides = this.state.activeGuides;
        if (!guides || guides.length == 0) {
            return null;
        }
        return guides.map(function (guide, idx) {
            var key = "m" + idx;
            switch (guide.guide.type) {
                case "x": {
                    var axisGuide = guide.guide;
                    return (React.createElement("line", { key: key, className: "snapping-guide", x1: axisGuide.value * _this.props.zoom.scale +
                            _this.props.zoom.centerX, x2: axisGuide.value * _this.props.zoom.scale +
                            _this.props.zoom.centerX, y1: 0, y2: _this.props.height }));
                }
                case "y": {
                    var axisGuide = guide.guide;
                    return (React.createElement("line", { key: key, className: "snapping-guide", y1: -axisGuide.value * _this.props.zoom.scale +
                            _this.props.zoom.centerY, y2: -axisGuide.value * _this.props.zoom.scale +
                            _this.props.zoom.centerY, x1: 0, x2: _this.props.width }));
                }
            }
        });
    };
    CreatingComponent.prototype.render = function () {
        var _this = this;
        return (React.createElement("g", { className: "creating-component" },
            this.renderSnappingGuides(),
            this.renderHint(),
            React.createElement("rect", { className: "interaction-handler", style: { cursor: "crosshair" }, ref: "handler", x: 0, y: 0, width: this.props.width, height: this.props.height, onMouseEnter: function () {
                    var move = function (e) {
                        var guides = __spread(_this.props.guides);
                        switch (_this.props.mode) {
                            case "hline":
                            case "vline":
                                // guides do not snap to anything
                                guides.length = 0;
                        }
                        var mgr = new PointSnapping(guides, 10 / _this.props.zoom.scale);
                        if (_this.isHammering) {
                            return;
                        }
                        var p = _this.getPointFromEvent({ x: e.pageX, y: e.pageY });
                        mgr.beginSnapping();
                        var hx = mgr.snapXValue(p.x);
                        var hy = mgr.snapYValue(p.y);
                        _this.setState({
                            activeGuides: Array.from(mgr.endSnapping()),
                            hoverCandidateX: hx,
                            hoverCandidateY: hy,
                        });
                    };
                    var leave = function () {
                        _this.refs.handler.removeEventListener("mousemove", move);
                        _this.refs.handler.removeEventListener("mouseleave", leave);
                    };
                    _this.refs.handler.addEventListener("mousemove", move);
                    _this.refs.handler.addEventListener("mouseleave", leave);
                } })));
    };
    return CreatingComponent;
}(React.Component));
exports.CreatingComponent = CreatingComponent;
var CreatingComponentFromCreatingInteraction = /** @class */ (function (_super) {
    __extends(CreatingComponentFromCreatingInteraction, _super);
    function CreatingComponentFromCreatingInteraction() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    CreatingComponentFromCreatingInteraction.prototype.doCreate = function (inMappings) {
        var desc = this.props.description;
        var mappings = {};
        var attributes = {};
        for (var attr in desc.mapping) {
            if (Object.prototype.hasOwnProperty.call(inMappings, attr)) {
                var name_1 = desc.mapping[attr];
                mappings[name_1] = inMappings[attr];
            }
        }
        for (var attr in desc.valueMappings) {
            mappings[attr] = [
                null,
                {
                    type: specification_1.MappingType.value,
                    value: desc.valueMappings[attr],
                },
            ];
        }
        for (var attr in desc.attributes) {
            attributes[attr] = desc.attributes[attr];
        }
        this.props.onCreate(mappings, attributes);
    };
    CreatingComponentFromCreatingInteraction.prototype.render = function () {
        var _this = this;
        var desc = this.props.description;
        var mode = "point";
        var onCreate = this
            .props.onCancel;
        function autoSwap(a, b) {
            if (a[0] < b[0]) {
                return [a, b];
            }
            else {
                return [b, a];
            }
        }
        switch (desc.type) {
            case "point":
                {
                    mode = "point";
                    onCreate = function (x, y) {
                        _this.doCreate({ x: x, y: y });
                    };
                }
                break;
            case "line-segment":
                {
                    mode = "line";
                    onCreate = function (x1, y1, x2, y2) {
                        _this.doCreate({ x1: x1, y1: y1, x2: x2, y2: y2 });
                    };
                }
                break;
            case "rectangle":
                {
                    mode = "rectangle";
                    onCreate = function (x1, y1, x2, y2) {
                        var _a, _b;
                        _a = __read(autoSwap(x1, x2), 2), x1 = _a[0], x2 = _a[1];
                        _b = __read(autoSwap(y1, y2), 2), y1 = _b[0], y2 = _b[1];
                        _this.doCreate({ xMin: x1, yMin: y1, xMax: x2, yMax: y2 });
                    };
                }
                break;
        }
        return (React.createElement(CreatingComponent, { width: this.props.width, height: this.props.height, zoom: this.props.zoom, guides: this.props.guides, mode: mode, onCancel: this.props.onCancel, onCreate: onCreate }));
    };
    return CreatingComponentFromCreatingInteraction;
}(React.Component));
exports.CreatingComponentFromCreatingInteraction = CreatingComponentFromCreatingInteraction;
//# sourceMappingURL=creating_component.js.map