"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.registerClasses = exports.SnapConstraintClass = exports.ConstraintTypeClass = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var common_1 = require("../../common");
var solver_1 = require("../../solver");
// Mark-level constraint
var ConstraintTypeClass = /** @class */ (function () {
    function ConstraintTypeClass() {
    }
    ConstraintTypeClass.register = function (entry) {
        ConstraintTypeClass._classes.set(entry.type, entry);
    };
    ConstraintTypeClass.getClass = function (type) {
        return ConstraintTypeClass._classes.get(type);
    };
    // Register and get mark class
    ConstraintTypeClass._classes = new Map();
    return ConstraintTypeClass;
}());
exports.ConstraintTypeClass = ConstraintTypeClass;
var SnapConstraintClass = /** @class */ (function () {
    function SnapConstraintClass() {
        this.type = "snap";
    }
    SnapConstraintClass.prototype.buildConstraints = function (constraint, elements, states, solver) {
        var _a = constraint.attributes, attribute = _a.attribute, element = _a.element, targetAttribute = _a.targetAttribute, targetElement = _a.targetElement;
        var gap = constraint.attributes.gap;
        if (gap == null) {
            gap = 0;
        }
        var idxElement = common_1.getIndexById(elements, element);
        var idxTargetElement = common_1.getIndexById(elements, targetElement);
        var attr = solver.attr(states[idxElement].attributes, attribute);
        var targetAttr = solver.attr(states[idxTargetElement].attributes, targetAttribute);
        solver.addLinear(solver_1.ConstraintStrength.HARD, gap, [
            [1, attr],
            [-1, targetAttr],
        ]);
    };
    return SnapConstraintClass;
}());
exports.SnapConstraintClass = SnapConstraintClass;
function registerClasses() {
    ConstraintTypeClass.register(new SnapConstraintClass());
}
exports.registerClasses = registerClasses;
//# sourceMappingURL=index.js.map