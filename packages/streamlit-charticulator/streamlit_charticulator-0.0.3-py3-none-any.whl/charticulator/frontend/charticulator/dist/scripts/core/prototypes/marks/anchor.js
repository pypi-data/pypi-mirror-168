"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
// Special element: Anchor
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
exports.AnchorElement = void 0;
var strings_1 = require("../../../strings");
var Specification = require("../../specification");
var specification_1 = require("../../specification");
var mark_1 = require("./mark");
var AnchorElement = /** @class */ (function (_super) {
    __extends(AnchorElement, _super);
    function AnchorElement() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /** Get a list of elemnt attributes */
        _this.attributeNames = ["x", "y"];
        _this.attributes = {
            x: {
                name: "x",
                type: Specification.AttributeType.Number,
            },
            y: {
                name: "y",
                type: Specification.AttributeType.Number,
            },
        };
        return _this;
    }
    /** Initialize the state of an element so that everything has a valid value */
    AnchorElement.prototype.initializeState = function () {
        var attrs = this.state.attributes;
        attrs.x = 0;
        attrs.y = 0;
    };
    /** Get bounding rectangle given current state */
    AnchorElement.prototype.getHandles = function () {
        return [];
        // let attrs = this.state.attributes as AnchorElementAttributes;
        // let { x, y } = attrs;
        // return [
        //     <Handles.Point>{
        //         type: "point",
        //         x: x, y: y,
        //         actions: []
        //     }
        // ]
    };
    // /** Get link anchors for this mark */
    // public getLinkAnchors(): LinkAnchor.Description[] {
    //     let attrs = this.state.attributes;
    //     return [
    //         {
    //             element: this.object._id,
    //             points: [
    //                 { x: attrs.x, y: attrs.y, xAttribute: "x", yAttribute: "y", direction: { x: 0, y: 1 } }
    //             ]
    //         }
    //     ];
    // }
    AnchorElement.createDefault = function (glyph) {
        var element = _super.createDefault.call(this, glyph);
        element.mappings.x = {
            type: specification_1.MappingType.parent,
            parentAttribute: "icx",
        };
        element.mappings.y = {
            type: specification_1.MappingType.parent,
            parentAttribute: "icy",
        };
        return element;
    };
    AnchorElement.prototype.getAttributePanelWidgets = function (manager) {
        return [manager.label(strings_1.strings.objects.anchor.label)];
    };
    AnchorElement.classID = "mark.anchor";
    AnchorElement.type = "mark";
    AnchorElement.metadata = {
        displayName: "Anchor",
        iconPath: "mark/anchor",
    };
    return AnchorElement;
}(mark_1.MarkClass));
exports.AnchorElement = AnchorElement;
//# sourceMappingURL=anchor.js.map