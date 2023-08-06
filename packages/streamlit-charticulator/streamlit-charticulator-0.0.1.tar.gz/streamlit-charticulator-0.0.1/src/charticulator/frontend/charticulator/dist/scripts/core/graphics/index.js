"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !exports.hasOwnProperty(p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * The module contains coordinate systems and classes for rendering elements(See {@link ChartRenderer} for details)
 *
 * @packageDocumentation
 * @preferred
 */
__exportStar(require("./elements"), exports);
__exportStar(require("./renderer"), exports);
var coordinate_system_1 = require("./coordinate_system");
Object.defineProperty(exports, "CoordinateSystem", { enumerable: true, get: function () { return coordinate_system_1.CoordinateSystem; } });
Object.defineProperty(exports, "CartesianCoordinates", { enumerable: true, get: function () { return coordinate_system_1.CartesianCoordinates; } });
Object.defineProperty(exports, "PolarCoordinates", { enumerable: true, get: function () { return coordinate_system_1.PolarCoordinates; } });
Object.defineProperty(exports, "BezierCurveCoordinates", { enumerable: true, get: function () { return coordinate_system_1.BezierCurveCoordinates; } });
Object.defineProperty(exports, "CoordinateSystemHelper", { enumerable: true, get: function () { return coordinate_system_1.CoordinateSystemHelper; } });
var bezier_curve_1 = require("./bezier_curve");
Object.defineProperty(exports, "BezierCurveParameterization", { enumerable: true, get: function () { return bezier_curve_1.BezierCurveParameterization; } });
Object.defineProperty(exports, "MultiCurveParametrization", { enumerable: true, get: function () { return bezier_curve_1.MultiCurveParametrization; } });
Object.defineProperty(exports, "LineSegmentParametrization", { enumerable: true, get: function () { return bezier_curve_1.LineSegmentParametrization; } });
//# sourceMappingURL=index.js.map