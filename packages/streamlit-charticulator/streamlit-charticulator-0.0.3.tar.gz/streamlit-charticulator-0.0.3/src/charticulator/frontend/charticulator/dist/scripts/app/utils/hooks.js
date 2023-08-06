"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.useLocalStorage = void 0;
var react_1 = require("react");
function useLocalStorage(initialValue, storageKey) {
    var _a = __read(react_1.useState(function () {
        try {
            var item = window.localStorage.getItem(storageKey);
            return item ? JSON.parse(item) : initialValue;
        }
        catch (ex) {
            console.log(ex);
            return initialValue;
        }
    }), 2), currentValue = _a[0], setCurrentValue = _a[1];
    var setValue = function (value) {
        try {
            window.localStorage.setItem(storageKey, JSON.stringify(value));
            setCurrentValue(value);
            return true;
        }
        catch (ex) {
            console.log(ex);
            return false;
        }
    };
    return [currentValue, setValue];
}
exports.useLocalStorage = useLocalStorage;
//# sourceMappingURL=hooks.js.map