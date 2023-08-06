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
exports.GuideCoordinatorClass = void 0;
var strings_1 = require("../../../strings");
var solver_1 = require("../../solver");
var Specification = require("../../specification");
var chart_element_1 = require("../chart_element");
var common_1 = require("../common");
var GuideCoordinatorClass = /** @class */ (function (_super) {
    __extends(GuideCoordinatorClass, _super);
    function GuideCoordinatorClass() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GuideCoordinatorClass.prototype.buildConstraints = function (solver) {
        var attrs = this.state.attributes;
        var t1, t2;
        if (this.getAxis() == "x") {
            t1 = solver.attr(attrs, "x1");
            t2 = solver.attr(attrs, "x2");
        }
        else {
            t1 = solver.attr(attrs, "y1");
            t2 = solver.attr(attrs, "y2");
        }
        var length = this.object.properties.count -
            GuideCoordinatorClass.BaseGuidesCount;
        this.getValueNames().map(function (name, index) {
            var t = (1 + index) / (length + 1);
            solver.addLinear(solver_1.ConstraintStrength.HARD, 0, [
                [1 - t, t1],
                [t, t2],
            ], [[1, solver.attr(attrs, name)]]);
        });
    };
    GuideCoordinatorClass.prototype.getValueNames = function () {
        var attrs = [];
        for (var i = 0; i <
            this.object.properties.count -
                GuideCoordinatorClass.BaseGuidesCount; i++) {
            var name_1 = "value" + i;
            attrs.push(name_1);
            if (this.state) {
                if (this.state.attributes[name_1] == null) {
                    this.state.attributes[name_1] = 0;
                }
            }
        }
        return attrs;
    };
    Object.defineProperty(GuideCoordinatorClass.prototype, "attributeNames", {
        get: function () {
            return ["x1", "y1", "x2", "y2"].concat(this.getValueNames());
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(GuideCoordinatorClass.prototype, "attributes", {
        get: function () {
            var r = {
                x1: {
                    name: "x1",
                    type: Specification.AttributeType.Number,
                },
                y1: {
                    name: "y1",
                    type: Specification.AttributeType.Number,
                },
                x2: {
                    name: "x2",
                    type: Specification.AttributeType.Number,
                },
                y2: {
                    name: "y2",
                    type: Specification.AttributeType.Number,
                },
            };
            for (var i = 0; i <
                this.object.properties.count -
                    GuideCoordinatorClass.BaseGuidesCount; i++) {
                var name_2 = "value" + i;
                r[name_2] = {
                    name: name_2,
                    type: Specification.AttributeType.Number,
                };
            }
            return r;
        },
        enumerable: false,
        configurable: true
    });
    GuideCoordinatorClass.prototype.initializeState = function () {
        var e_1, _a;
        this.state.attributes.x1 = -100;
        this.state.attributes.y1 = -100;
        this.state.attributes.x2 = 100;
        this.state.attributes.y2 = 100;
        try {
            for (var _b = __values(this.getValueNames()), _c = _b.next(); !_c.done; _c = _b.next()) {
                var name_3 = _c.value;
                if (this.state.attributes[name_3] == null) {
                    this.state.attributes[name_3] = 0;
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
    };
    GuideCoordinatorClass.prototype.getAxis = function () {
        return this.object.properties.axis;
    };
    /** Get handles given current state */
    GuideCoordinatorClass.prototype.getHandles = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1, x2 = attrs.x2, y2 = attrs.y2;
        var axis = this.getAxis();
        return [
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
                x: axis == "y" ? x1 : x2,
                y: axis == "x" ? y1 : y2,
                actions: [
                    {
                        type: "attribute",
                        source: "x",
                        attribute: axis == "y" ? "x1" : "x2",
                    },
                    {
                        type: "attribute",
                        source: "y",
                        attribute: axis == "x" ? "y1" : "y2",
                    },
                ],
            },
        ];
    };
    GuideCoordinatorClass.prototype.getBoundingBox = function () {
        var attrs = this.state.attributes;
        var x1 = attrs.x1, y1 = attrs.y1;
        var x2 = attrs.x2, y2 = attrs.y2;
        if (this.getAxis() == "x") {
            y2 = y1;
        }
        else {
            x2 = x1;
        }
        return {
            type: "line",
            visible: true,
            morphing: true,
            x1: x1,
            y1: y1,
            x2: x2,
            y2: y2,
        };
    };
    GuideCoordinatorClass.prototype.getBasicValues = function () {
        return [];
        // uncomment to render main mark guides
        // if (this.getAxis() === "x") {
        //   return ["x1", "x2"];
        // }
        // if (this.getAxis() === "y") {
        //   return ["y1", "y2"];
        // }
    };
    GuideCoordinatorClass.prototype.getSnappingGuides = function () {
        var _this = this;
        return this.getValueNames()
            .concat(this.getBasicValues())
            .map(function (name) {
            return {
                type: _this.getAxis(),
                value: _this.state.attributes[name],
                attribute: name,
                visible: true,
                visualType: common_1.SnappingGuidesVisualTypes.Coordinator,
                priority: 1,
            };
        });
    };
    /** Get controls given current state */
    GuideCoordinatorClass.prototype.getAttributePanelWidgets = function (manager) {
        return [
            manager.verticalGroup({ header: strings_1.strings.objects.guides.guideCoordinator }, [
                manager.inputNumber({ property: "count" }, {
                    showUpdown: true,
                    updownTick: 1,
                    updownRange: [1, 100],
                    minimum: 1,
                    maximum: 100,
                    label: strings_1.strings.objects.guides.count,
                    searchSection: strings_1.strings.objects.guides.guideCoordinator,
                }),
            ]),
        ];
    };
    GuideCoordinatorClass.classID = "guide.guide-coordinator";
    GuideCoordinatorClass.type = "guide";
    GuideCoordinatorClass.BaseGuidesCount = 0;
    GuideCoordinatorClass.metadata = {
        displayName: "GuideCoordinator",
        iconPath: "guide/coordinator-x",
    };
    GuideCoordinatorClass.defaultAttributes = {
        axis: "x",
        count: 2,
    };
    return GuideCoordinatorClass;
}(chart_element_1.ChartElementClass));
exports.GuideCoordinatorClass = GuideCoordinatorClass;
//# sourceMappingURL=guide_coordinator.js.map