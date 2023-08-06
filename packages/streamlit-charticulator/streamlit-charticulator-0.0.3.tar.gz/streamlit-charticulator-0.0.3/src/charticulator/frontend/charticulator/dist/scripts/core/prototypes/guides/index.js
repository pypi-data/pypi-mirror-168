"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
Object.defineProperty(exports, "__esModule", { value: true });
exports.registerClasses = void 0;
var object_1 = require("../object");
var guide_coordinator_1 = require("./guide_coordinator");
var polar_coordinator_1 = require("./polar_coordinator");
var guide_1 = require("./guide");
var guide_2 = require("./guide");
Object.defineProperty(exports, "GuideClass", { enumerable: true, get: function () { return guide_2.GuideClass; } });
Object.defineProperty(exports, "GuideAttributeNames", { enumerable: true, get: function () { return guide_2.GuideAttributeNames; } });
Object.defineProperty(exports, "GuidePropertyNames", { enumerable: true, get: function () { return guide_2.GuidePropertyNames; } });
var guide_coordinator_2 = require("./guide_coordinator");
Object.defineProperty(exports, "GuideCoordinatorClass", { enumerable: true, get: function () { return guide_coordinator_2.GuideCoordinatorClass; } });
var polar_coordinator_2 = require("./polar_coordinator");
Object.defineProperty(exports, "GuidePolarCoordinatorClass", { enumerable: true, get: function () { return polar_coordinator_2.GuidePolarCoordinatorClass; } });
function registerClasses() {
    object_1.ObjectClasses.Register(guide_1.GuideClass);
    object_1.ObjectClasses.Register(guide_coordinator_1.GuideCoordinatorClass);
    object_1.ObjectClasses.Register(polar_coordinator_1.GuidePolarCoordinatorClass);
}
exports.registerClasses = registerClasses;
//# sourceMappingURL=index.js.map