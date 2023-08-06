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
exports.GuidePolarCoordinatorClass = exports.getPointValueName = exports.getRadialValueName = exports.getAngularValueName = exports.PolarGuideBaseAttributeNames = exports.PolarGuidePropertyNames = void 0;
var strings_1 = require("../../../strings");
var solver_1 = require("../../solver");
var Specification = require("../../specification");
var chart_element_1 = require("../chart_element");
exports.PolarGuidePropertyNames = [
    "angularGuidesCount",
    "endAngle",
    "innerRatio",
    "outerRatio",
    "radialGuidesCount",
    "startAngle",
];
exports.PolarGuideBaseAttributeNames = ["x", "y", "x1", "y1", "x2", "y2", "angle1", "angle2", "radial1"];
exports.getAngularValueName = function (index) { return "angularValue" + index; };
exports.getRadialValueName = function (index) { return "radialValue" + index; };
exports.getPointValueName = function (angularIndex, radialIndex, axis) { return "point" + angularIndex + radialIndex + axis; };
var GuidePolarCoordinatorClass = /** @class */ (function (_super) {
    __extends(GuidePolarCoordinatorClass, _super);
    function GuidePolarCoordinatorClass() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    // eslint-disable-next-line
    GuidePolarCoordinatorClass.prototype.buildConstraints = function (solver, 
    // eslint-disable-next-line
    constr, manager) {
        var attrs = this.state.attributes;
        var props = this.object.properties;
        var radialY = this.getValueNamesForRadial();
        var chunkSizeY = (1 - 0) / radialY.length;
        var chunkRangesY = radialY.map(function (c, i) {
            return [
                0 + (0 + chunkSizeY) * i,
                0 + (0 + chunkSizeY) * i + chunkSizeY,
            ];
        });
        var angularX = this.getValueNamesForAngular();
        var chunkSizeX = (1 - 0) / angularX.length;
        var chunkRangesX = angularX.map(function (c, i) {
            return [
                0 + (0 + chunkSizeX) * i,
                0 + (0 + chunkSizeX) * i + chunkSizeX,
            ];
        });
        var _a = __read(solver.attrs(attrs, [
            "x",
            "y",
            "x1",
            "x2",
            "y1",
            "y2",
            "angle1",
            "angle2",
            "radial1",
            "radial2",
        ]), 10), x = _a[0], y = _a[1], x1 = _a[2], x2 = _a[3], y1 = _a[4], y2 = _a[5], angle1 = _a[6], angle2 = _a[7], innerRadius = _a[8], outerRadius = _a[9];
        attrs.angle1 = props.startAngle;
        attrs.angle2 = props.endAngle;
        solver.makeConstant(attrs, "angle1");
        solver.makeConstant(attrs, "angle2");
        if (Math.abs(attrs.x2 - attrs.x1) < Math.abs(attrs.y2 - attrs.y1)) {
            attrs.radial1 = (props.innerRatio * (attrs.x2 - attrs.x1)) / 2;
            attrs.radial2 = (props.outerRatio * (attrs.x2 - attrs.x1)) / 2;
            // innerRatio * x2 - innerRatio * x1 = 2 * innerRadius
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                [props.innerRatio, x2],
                [-props.innerRatio, x1],
            ], [[2, innerRadius]]);
            // outerRatio * x2 - outerRatio * x1 = 2 * outerRadius
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                [props.outerRatio, x2],
                [-props.outerRatio, x1],
            ], [[2, outerRadius]]);
        }
        else {
            attrs.radial1 = (props.innerRatio * (attrs.y2 - attrs.y1)) / 2;
            attrs.radial2 = (props.outerRatio * (attrs.y2 - attrs.y1)) / 2;
            // innerRatio * y2 - innerRatio * y1 = 2 * innerRadius
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                [props.innerRatio, y2],
                [-props.innerRatio, y1],
            ], [[2, innerRadius]]);
            // outerRatio * y2 - outerRatio * y1 = 2 * outerRadius
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                [props.outerRatio, y2],
                [-props.outerRatio, y1],
            ], [[2, outerRadius]]);
        }
        // add constraint 2 * x = x1 + x2
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[2, x]], [
            [1, x1],
            [1, x2],
        ]);
        // add constraint 2 * y = y1 + y2
        solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [[2, y]], [
            [1, y1],
            [1, y2],
        ]);
        // xy
        {
            var angleVarable = [];
            for (var xindex = 0; xindex < angularX.length; xindex++) {
                angleVarable.push(solver.attr(attrs, angularX[xindex]));
            }
            var radialVarable = [];
            for (var yindex = 0; yindex < radialY.length; yindex++) {
                radialVarable.push(solver.attr(attrs, radialY[yindex]));
            }
            for (var xindex = 0; xindex < angularX.length; xindex++) {
                var _b = __read(chunkRangesX[xindex], 2), t1 = _b[0], t2 = _b[1];
                var vx1Expr = [
                    [t1, angle2],
                    [1 - t1, angle1],
                ];
                var vx2Expr = [
                    [t2, angle2],
                    [1 - t2, angle1],
                ];
                var vx1 = solver.attr({ value: solver.getLinear.apply(solver, __spread(vx1Expr)) }, "valueX", { edit: true });
                var vx2 = solver.attr({ value: solver.getLinear.apply(solver, __spread(vx2Expr)) }, "valueX", { edit: true });
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, vx1Expr, [[1, vx1]]);
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, vx2Expr, [[1, vx2]]);
                solver.addEquals(solver_1.ConstraintStrength.HARD, solver.attr(attrs, angularX[xindex], {
                    edit: false,
                }), vx1);
            }
            for (var yindex = 0; yindex < radialY.length; yindex++) {
                var _c = __read(chunkRangesY[yindex], 2), t1 = _c[0], t2 = _c[1];
                var vy1Expr = [
                    [t1, outerRadius],
                    [1 - t1, innerRadius],
                ];
                var vy2Expr = [
                    [t2, outerRadius],
                    [1 - t2, innerRadius],
                ];
                var vy1 = solver.attr({ value: solver.getLinear.apply(solver, __spread(vy1Expr)) }, "valueY", { edit: true });
                var vy2 = solver.attr({ value: solver.getLinear.apply(solver, __spread(vy2Expr)) }, "valueY", { edit: true });
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, vy1Expr, [[1, vy1]]);
                solver.addLinear(solver_1.ConstraintStrength.HARD, 0, vy2Expr, [[1, vy2]]);
                solver.addEquals(solver_1.ConstraintStrength.HARD, solver.attr(attrs, radialY[yindex], {
                    edit: false,
                }), vy2);
            }
            var chartConstraints = this.parent.object.constraints;
            solver.addPlugin(new solver_1.ConstraintPlugins.PolarCoordinatorPlugin(solver, x, y, radialVarable, angleVarable, attrs, chartConstraints, this.object._id, manager));
        }
    };
    GuidePolarCoordinatorClass.prototype.getValueNamesForAngular = function () {
        var attrs = [];
        for (var i = 0; i < this.object.properties.angularGuidesCount; i++) {
            var name_1 = exports.getAngularValueName(i);
            attrs.push(name_1);
            if (this.state) {
                if (this.state.attributes[name_1] == null) {
                    this.state.attributes[name_1] = 0;
                }
            }
        }
        return attrs;
    };
    GuidePolarCoordinatorClass.prototype.getValueNamesForRadial = function () {
        var attrs = [];
        for (var i = 0; i < this.object.properties.radialGuidesCount; i++) {
            var name_2 = exports.getRadialValueName(i);
            attrs.push(name_2);
            if (this.state) {
                if (this.state.attributes[name_2] == null) {
                    this.state.attributes[name_2] = 0;
                }
            }
        }
        return attrs;
    };
    GuidePolarCoordinatorClass.prototype.getValueNamesForPoints = function () {
        var attrs = [];
        for (var i = 0; i < this.object.properties.angularGuidesCount; i++) {
            for (var j = 0; j < this.object.properties.radialGuidesCount; j++) {
                var nameX = exports.getPointValueName(i, j, "X");
                attrs.push(nameX);
                if (this.state) {
                    if (this.state.attributes[nameX] == null) {
                        this.state.attributes[nameX] = 0;
                    }
                }
                var nameY = exports.getPointValueName(i, j, "Y");
                attrs.push(nameY);
                if (this.state) {
                    if (this.state.attributes[nameX] == null) {
                        this.state.attributes[nameX] = 0;
                    }
                }
            }
        }
        return attrs;
    };
    Object.defineProperty(GuidePolarCoordinatorClass.prototype, "attributeNames", {
        get: function () {
            return exports.PolarGuideBaseAttributeNames.concat(this.getValueNamesForAngular()).concat(this.getValueNamesForRadial());
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(GuidePolarCoordinatorClass.prototype, "attributes", {
        get: function () {
            var attributesType = this.attributeNames.map(function (name) {
                return {
                    name: name,
                    type: Specification.AttributeType.Number,
                };
            });
            var attributes = {};
            attributesType.forEach(function (attr) { return (attributes[attr.name] = attr); });
            return attributes;
        },
        enumerable: false,
        configurable: true
    });
    GuidePolarCoordinatorClass.prototype.initializeState = function () {
        var e_1, _a, e_2, _b, e_3, _c;
        var attrs = this.state.attributes;
        attrs.angle1 = 0;
        attrs.angle2 = 360;
        attrs.radial1 = 10;
        attrs.radial2 = 100;
        attrs.x1 = -100;
        attrs.x2 = 100;
        attrs.y1 = -100;
        attrs.y2 = 100;
        attrs.x = attrs.x1;
        attrs.y = attrs.y2;
        attrs.gapX = 4;
        attrs.gapY = 4;
        try {
            for (var _d = __values(this.getValueNamesForAngular()), _e = _d.next(); !_e.done; _e = _d.next()) {
                var name_3 = _e.value;
                if (this.state.attributes[name_3] == null) {
                    this.state.attributes[name_3] = 0;
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_e && !_e.done && (_a = _d.return)) _a.call(_d);
            }
            finally { if (e_1) throw e_1.error; }
        }
        try {
            for (var _f = __values(this.getValueNamesForRadial()), _g = _f.next(); !_g.done; _g = _f.next()) {
                var name_4 = _g.value;
                if (this.state.attributes[name_4] == null) {
                    this.state.attributes[name_4] = 0;
                }
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_g && !_g.done && (_b = _f.return)) _b.call(_f);
            }
            finally { if (e_2) throw e_2.error; }
        }
        try {
            for (var _h = __values(this.getValueNamesForPoints()), _j = _h.next(); !_j.done; _j = _h.next()) {
                var name_5 = _j.value;
                if (this.state.attributes[name_5] == null) {
                    this.state.attributes[name_5] = 0;
                }
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (_j && !_j.done && (_c = _h.return)) _c.call(_h);
            }
            finally { if (e_3) throw e_3.error; }
        }
    };
    /** Get handles given current state */
    GuidePolarCoordinatorClass.prototype.getHandles = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        return [
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
    };
    GuidePolarCoordinatorClass.prototype.getBoundingBox = function () {
        var attrs = this.state.attributes;
        var x = attrs.x, y = attrs.y, x2 = attrs.x2, y2 = attrs.y2, x1 = attrs.x1, y1 = attrs.y1;
        var radial2 = 0;
        if (Math.abs(x2 - x1) < Math.abs(y2 - y1)) {
            radial2 = (this.object.properties.outerRatio * (x2 - x1)) / 2;
        }
        else {
            radial2 = (this.object.properties.outerRatio * (y2 - y1)) / 2;
        }
        return {
            type: "circle",
            cx: x,
            cy: y,
            radius: Math.abs(radial2),
        };
    };
    GuidePolarCoordinatorClass.prototype.getSnappingGuides = function () {
        var result = [];
        for (var i = 0; i < this.object.properties.angularGuidesCount; i++) {
            for (var j = 0; j < this.object.properties.radialGuidesCount; j++) {
                var nameX = exports.getPointValueName(i, j, "X");
                var nameY = exports.getPointValueName(i, j, "Y");
                result.push({
                    type: "point",
                    angle: this.state.attributes[nameX],
                    radius: this.state.attributes[nameY],
                    startAngle: this.object.properties.startAngle,
                    endAngle: this.object.properties.endAngle,
                    angleAttribute: nameX,
                    radiusAttribute: nameY,
                    visible: true,
                    cx: this.state.attributes.x,
                    cy: this.state.attributes.y,
                    visibleAngle: this.state.attributes[exports.getAngularValueName(i)],
                    visibleRadius: this.state.attributes[exports.getRadialValueName(j)],
                });
            }
        }
        // add center for coordinates
        result.push({
            type: "point",
            angle: this.state.attributes.x,
            radius: this.state.attributes.y,
            startAngle: this.object.properties.startAngle,
            endAngle: this.object.properties.endAngle,
            angleAttribute: "x",
            radiusAttribute: "y",
            visible: true,
            cx: this.state.attributes.x,
            cy: this.state.attributes.y,
            visibleAngle: 0,
            visibleRadius: 0,
        });
        return result;
    };
    /** Get controls given current state */
    GuidePolarCoordinatorClass.prototype.getAttributePanelWidgets = function (manager) {
        return [
            manager.verticalGroup({ header: strings_1.strings.objects.guides.guideCoordinator }, [
                manager.inputNumber({ property: "angularGuidesCount" }, {
                    showUpdown: true,
                    updownTick: 1,
                    updownRange: [1, 100],
                    minimum: 2,
                    maximum: 100,
                    label: strings_1.strings.objects.guides.angular,
                    searchSection: strings_1.strings.objects.guides.guideCoordinator,
                }),
                // uncomment to allow configure count of guides in different radiuses
                // manager.row(
                //   strings.objects.guides.radial,
                //   manager.inputNumber(
                //     { property: "radialGuidesCount" },
                //     {
                //       showUpdown: true,
                //       updownTick: 1,
                //       updownRange: [1, 100],
                //       minimum: 1,
                //       maximum: 100,
                //     }
                //   )
                // ),
                manager.searchWrapper({
                    searchPattern: [
                        strings_1.strings.objects.guides.angle,
                        strings_1.strings.objects.guides.guideCoordinator,
                    ],
                }, manager.vertical(manager.label(strings_1.strings.objects.guides.angle), manager.horizontal([1, 0, 1], manager.inputNumber({ property: "startAngle" }, { ignoreSearch: true }), manager.label("-"), manager.inputNumber({ property: "endAngle" }, { ignoreSearch: true })))),
            ]),
        ];
    };
    GuidePolarCoordinatorClass.classID = "guide.guide-coordinator-polar";
    GuidePolarCoordinatorClass.type = "guide";
    GuidePolarCoordinatorClass.metadata = {
        displayName: "GuidePolarCoordinator",
        iconPath: "guide/coordinator-polar",
        creatingInteraction: {
            type: "rectangle",
            mapping: { xMin: "x1", yMin: "y1", xMax: "x2", yMax: "y2" },
        },
    };
    GuidePolarCoordinatorClass.defaultAttributes = {
        angularGuidesCount: 4,
        radialGuidesCount: 4,
    };
    return GuidePolarCoordinatorClass;
}(chart_element_1.ChartElementClass));
exports.GuidePolarCoordinatorClass = GuidePolarCoordinatorClass;
//# sourceMappingURL=polar_coordinator.js.map