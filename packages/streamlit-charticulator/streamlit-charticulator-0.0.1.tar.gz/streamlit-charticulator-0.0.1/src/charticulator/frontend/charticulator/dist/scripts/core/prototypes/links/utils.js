"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
Object.defineProperty(exports, "__esModule", { value: true });
exports.shouldShowCloseLink = void 0;
var plot_segments_1 = require("../plot_segments");
function shouldShowCloseLink(parent, linkProperties, userClose) {
    if (linkProperties.linkTable) {
        return false;
    }
    if (!parent) {
        return false;
    }
    if (!parent.object.elements) {
        return false;
    }
    if (linkProperties.linkThrough) {
        var plotSegment = parent.object.elements.find(function (element) { return element._id == linkProperties.linkThrough.plotSegment; });
        if ((plotSegment === null || plotSegment === void 0 ? void 0 : plotSegment.classID) == plot_segments_1.PolarPlotSegment.classID) {
            if (userClose) {
                return linkProperties.closeLink;
            }
            return true;
        }
    }
    return false;
}
exports.shouldShowCloseLink = shouldShowCloseLink;
//# sourceMappingURL=utils.js.map