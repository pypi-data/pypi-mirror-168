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
Object.defineProperty(exports, "__esModule", { value: true });
exports.ScaleClass = void 0;
var common_1 = require("../common");
var ScaleClass = /** @class */ (function (_super) {
    __extends(ScaleClass, _super);
    function ScaleClass() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    // eslint-disable-next-line
    ScaleClass.prototype.buildConstraint = function (
    // eslint-disable-next-line
    data, 
    // eslint-disable-next-line
    target, 
    // eslint-disable-next-line
    solver
    // eslint-disable-next-line
    ) { };
    ScaleClass.prototype.getTemplateParameters = function () {
        return {
            inferences: [
                {
                    objectID: this.object._id,
                    autoDomainMax: this.object.properties.autoDomainMax,
                    autoDomainMin: this.object.properties.autoDomainMin,
                    scale: {
                        classID: this.object.classID,
                        expressions: [],
                        properties: {
                            mapping: "mapping",
                        },
                    },
                },
            ],
        };
    };
    ScaleClass.metadata = {
        displayName: "Scale",
        iconPath: "scale/scale",
    };
    return ScaleClass;
}(common_1.ObjectClass));
exports.ScaleClass = ScaleClass;
//# sourceMappingURL=scale.js.map