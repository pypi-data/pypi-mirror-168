"use strict";
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
exports.isType = exports.ObjectClasses = exports.ObjectClass = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var common_1 = require("../common");
var specification_1 = require("../specification");
var strings_1 = require("../../strings");
/** A ObjectClass contains the runtime info for a chart object */
var ObjectClass = /** @class */ (function () {
    function ObjectClass(parent, object, state) {
        this.parent = parent;
        this.object = object;
        this.state = state;
    }
    /** Initialize the state of the object */
    // eslint-disable-next-line
    ObjectClass.prototype.initializeState = function () { };
    /** Get the UI spec for property panel */
    ObjectClass.prototype.getAttributePanelWidgets = function (manager) {
        return [
            manager.verticalGroup({
                header: strings_1.strings.objects.interactivity,
            }, [
                manager.inputBoolean({ property: "enableTooltips" }, {
                    type: "checkbox",
                    label: strings_1.strings.objects.toolTips,
                    searchSection: strings_1.strings.objects.interactivity,
                }),
                manager.inputBoolean({ property: "enableContextMenu" }, {
                    type: "checkbox",
                    label: strings_1.strings.objects.contextMenu,
                    searchSection: strings_1.strings.objects.interactivity,
                }),
                manager.inputBoolean({ property: "enableSelection" }, {
                    type: "checkbox",
                    label: strings_1.strings.objects.selection,
                    searchSection: strings_1.strings.objects.interactivity,
                }),
            ]),
        ];
    };
    ObjectClass.prototype.getTemplateParameters = function () {
        return null;
    };
    /** Create a default object */
    // eslint-disable-next-line
    ObjectClass.createDefault = function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        var id = common_1.uniqueID();
        var obj = {
            _id: id,
            classID: this.classID,
            properties: {},
            mappings: {},
        };
        obj.properties = common_1.deepClone(this.defaultProperties);
        for (var attr in this.defaultMappingValues) {
            if (Object.prototype.hasOwnProperty.call(this.defaultMappingValues, attr)) {
                var value = common_1.deepClone(this.defaultMappingValues[attr]);
                obj.mappings[attr] = {
                    type: specification_1.MappingType.value,
                    value: value,
                };
            }
        }
        return obj;
    };
    /** The static classID */
    ObjectClass.classID = "object";
    /** The static type */
    ObjectClass.type = null;
    /** The metadata associated with the class */
    ObjectClass.metadata = {};
    /** Default attributes */
    ObjectClass.defaultProperties = {
        enableTooltips: true,
        enableContextMenu: true,
        enableSelection: true,
        exposed: true,
    };
    /** Default mapping values */
    ObjectClass.defaultMappingValues = {};
    return ObjectClass;
}());
exports.ObjectClass = ObjectClass;
/** Store the registered object classes */
var ObjectClasses = /** @class */ (function () {
    function ObjectClasses() {
    }
    /** Create a ObjectClass for a object and its state */
    ObjectClasses.Create = function (parent, object, state) {
        var constructor = ObjectClasses.registeredObjectClasses.get(object.classID);
        if (!constructor) {
            throw new Error("undefined object class '" + object.classID + "'");
        }
        return new constructor(parent, object, state);
    };
    ObjectClasses.CreateDefault = function (classID) {
        var args = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            args[_i - 1] = arguments[_i];
        }
        var constructor = ObjectClasses.registeredObjectClasses.get(classID);
        var obj = constructor.createDefault.apply(constructor, __spread(args));
        return obj;
    };
    ObjectClasses.GetMetadata = function (classID) {
        var constructor = ObjectClasses.registeredObjectClasses.get(classID);
        if (constructor) {
            return constructor.metadata || null;
        }
        else {
            return null;
        }
    };
    ObjectClasses.Register = function (constructor) {
        ObjectClasses.registeredObjectClasses.set(constructor.classID, constructor);
        if (constructor.type != null) {
            ObjectClasses.RegisterType(constructor.classID, constructor.type);
        }
    };
    ObjectClasses.RegisterType = function (name) {
        var parents = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            parents[_i - 1] = arguments[_i];
        }
        ObjectClasses.type2Parents.set(name, parents);
    };
    ObjectClasses.isType = function (type, parentType) {
        if (type == parentType) {
            return true;
        }
        var parents = ObjectClasses.type2Parents.get(type);
        if (parents != null) {
            return parents.some(function (t) { return ObjectClasses.isType(t, parentType); });
        }
        else {
            return false;
        }
    };
    /**
     * Gets an interator of registered classes.
     */
    ObjectClasses.RegisteredClasses = function () {
        return this.registeredObjectClasses.values();
    };
    ObjectClasses.registeredObjectClasses = new Map();
    ObjectClasses.type2Parents = new Map();
    return ObjectClasses;
}());
exports.ObjectClasses = ObjectClasses;
exports.isType = ObjectClasses.isType;
//# sourceMappingURL=object.js.map