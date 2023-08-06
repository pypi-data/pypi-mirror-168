"use strict";
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
exports.replaceUndefinedByNull = exports.expect_deep_approximately_equals = exports.getAligntment = exports.isInIFrame = exports.copyToClipboard = exports.convertColumns = exports.getConvertableTypes = exports.getPreferredDataKind = exports.getConvertableDataKind = exports.stringToDataURL = exports.b64EncodeUnicode = exports.showOpenFileDialog = exports.getFileNameWithoutExtension = exports.getExtensionFromFileName = exports.readFileAsDataUrl = exports.readFileAsString = exports.renderDataURLToPNG = exports.parseHashString = exports.toSVGZoom = exports.toSVGNumber = exports.classNames = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var core_1 = require("../../core");
var specification_1 = require("../../core/specification");
var data_types_1 = require("../../core/dataset/data_types");
var chai_1 = require("chai");
function classNames() {
    var args = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        args[_i] = arguments[_i];
    }
    return args
        .filter(function (x) { return x != null && (typeof x == "string" || x[1] == true); })
        .map(function (x) { return (typeof x == "string" ? x : x[0]); })
        .join(" ");
}
exports.classNames = classNames;
function toSVGNumber(x) {
    return core_1.prettyNumber(x, 8);
}
exports.toSVGNumber = toSVGNumber;
function toSVGZoom(zoom) {
    return "translate(" + core_1.prettyNumber(zoom.centerX) + "," + core_1.prettyNumber(zoom.centerY) + ") scale(" + core_1.prettyNumber(zoom.scale) + ")";
}
exports.toSVGZoom = toSVGZoom;
function parseHashString(value) {
    // Make sure value doesn't start with "#" or "#!"
    if (value[0] == "#") {
        value = value.substr(1);
    }
    if (value[0] == "!") {
        value = value.substr(1);
    }
    // Split by & and parse each key=value pair
    return value.split("&").reduce(function (prev, str) {
        var pair = str.split("=");
        prev[decodeURIComponent(pair[0])] =
            pair.length == 2 ? decodeURIComponent(pair[1]) : "";
        return prev;
    }, {});
}
exports.parseHashString = parseHashString;
function renderDataURLToPNG(dataurl, options) {
    return new Promise(function (resolve, reject) {
        var img = new Image();
        img.src = dataurl;
        img.onload = function () {
            var width = img.width;
            var height = img.height;
            var canvas = document.createElement("canvas");
            var ctx = canvas.getContext("2d");
            switch (options.mode) {
                case "scale":
                    {
                        canvas.width = width * options.scale;
                        canvas.height = height * options.scale;
                        if (options.background) {
                            ctx.fillStyle = options.background;
                            ctx.fillRect(0, 0, canvas.width, canvas.height);
                        }
                        ctx.scale(options.scale, options.scale);
                        ctx.drawImage(img, 0, 0);
                    }
                    break;
                case "thumbnail":
                    {
                        canvas.width = options.thumbnail[0];
                        canvas.height = options.thumbnail[1];
                        if (options.background) {
                            ctx.fillStyle = options.background;
                            ctx.fillRect(0, 0, canvas.width, canvas.height);
                        }
                        var maxScale = Math.max(canvas.width / width, canvas.height / height);
                        ctx.scale(maxScale, maxScale);
                        ctx.drawImage(img, 0, 0);
                    }
                    break;
            }
            resolve(canvas);
        };
        img.onerror = function () {
            reject(new Error("failed to load image"));
        };
    });
}
exports.renderDataURLToPNG = renderDataURLToPNG;
function readFileAsString(file) {
    return new Promise(function (resolve, reject) {
        var reader = new FileReader();
        reader.onload = function () {
            resolve(reader.result);
        };
        reader.onerror = function () {
            reject(new Error("unable to read file " + file.name));
        };
        reader.readAsText(file, "utf-8");
    });
}
exports.readFileAsString = readFileAsString;
function readFileAsDataUrl(file) {
    return new Promise(function (resolve, reject) {
        var reader = new FileReader();
        reader.onload = function () {
            resolve(reader.result);
        };
        reader.onerror = function () {
            reject(new Error("unable to read file " + file.name));
        };
        reader.readAsDataURL(file);
    });
}
exports.readFileAsDataUrl = readFileAsDataUrl;
function getExtensionFromFileName(filename) {
    var m = filename.match(/\.([^.]+)$/);
    if (m) {
        return m[1].toLowerCase();
    }
    else {
        return null;
    }
}
exports.getExtensionFromFileName = getExtensionFromFileName;
function getFileNameWithoutExtension(filename) {
    return filename.replace(/\.([^.]+)$/, "");
}
exports.getFileNameWithoutExtension = getFileNameWithoutExtension;
function showOpenFileDialog(accept) {
    return new Promise(function (resolve, reject) {
        var inputElement = document.createElement("input");
        inputElement.type = "file";
        if (accept != null) {
            inputElement.accept = accept.map(function (x) { return "." + x; }).join(",");
        }
        inputElement.onchange = function () {
            if (inputElement.files.length == 1) {
                resolve(inputElement.files[0]);
            }
            else {
                reject();
            }
        };
        inputElement.click();
    });
}
exports.showOpenFileDialog = showOpenFileDialog;
function b64EncodeUnicode(str) {
    return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, function (match, p1) {
        return String.fromCharCode(parseInt(p1, 16));
    }));
}
exports.b64EncodeUnicode = b64EncodeUnicode;
function stringToDataURL(mimeType, content) {
    return "data:" + mimeType + ";base64," + b64EncodeUnicode(content);
}
exports.stringToDataURL = stringToDataURL;
function checkConvertion(type, dataSample) {
    var e_1, _a, e_2, _b, e_3, _c;
    var convertable = true;
    if (type === specification_1.DataType.String) {
        return convertable;
    }
    switch (type) {
        case specification_1.DataType.Boolean:
            try {
                for (var dataSample_1 = __values(dataSample), dataSample_1_1 = dataSample_1.next(); !dataSample_1_1.done; dataSample_1_1 = dataSample_1.next()) {
                    var data = dataSample_1_1.value;
                    if (data &&
                        data.toString().toLowerCase() != "0" &&
                        data.toString().toLowerCase() != "true" &&
                        data.toString().toLowerCase() != "1" &&
                        data.toString().toLowerCase() != "false" &&
                        data.toString().toLowerCase() != "yes" &&
                        data.toString().toLowerCase() != "no") {
                        convertable = false;
                        break;
                    }
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (dataSample_1_1 && !dataSample_1_1.done && (_a = dataSample_1.return)) _a.call(dataSample_1);
                }
                finally { if (e_1) throw e_1.error; }
            }
            return convertable;
        case specification_1.DataType.Date:
            convertable = true;
            try {
                for (var dataSample_2 = __values(dataSample), dataSample_2_1 = dataSample_2.next(); !dataSample_2_1.done; dataSample_2_1 = dataSample_2.next()) {
                    var data = dataSample_2_1.value;
                    if (data &&
                        Number.isNaN(Date.parse(data.toString())) &&
                        Number.isNaN(new Date(+data.toString()).getDate())) {
                        convertable = false;
                        break;
                    }
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (dataSample_2_1 && !dataSample_2_1.done && (_b = dataSample_2.return)) _b.call(dataSample_2);
                }
                finally { if (e_2) throw e_2.error; }
            }
            return convertable;
        case specification_1.DataType.Number:
            convertable = true;
            try {
                for (var dataSample_3 = __values(dataSample), dataSample_3_1 = dataSample_3.next(); !dataSample_3_1.done; dataSample_3_1 = dataSample_3.next()) {
                    var data = dataSample_3_1.value;
                    if (data && Number.isNaN(Number.parseFloat(data.toString()))) {
                        convertable = false;
                        break;
                    }
                }
            }
            catch (e_3_1) { e_3 = { error: e_3_1 }; }
            finally {
                try {
                    if (dataSample_3_1 && !dataSample_3_1.done && (_c = dataSample_3.return)) _c.call(dataSample_3);
                }
                finally { if (e_3) throw e_3.error; }
            }
            return convertable;
        default:
            return false;
    }
}
function getConvertableDataKind(type) {
    var kinds;
    switch (type) {
        case specification_1.DataType.Boolean:
            kinds = [specification_1.DataKind.Categorical, specification_1.DataKind.Ordinal];
            break;
        case specification_1.DataType.Date:
            kinds = [specification_1.DataKind.Categorical, specification_1.DataKind.Ordinal, specification_1.DataKind.Temporal];
            break;
        case specification_1.DataType.String:
            kinds = [specification_1.DataKind.Categorical, specification_1.DataKind.Ordinal];
            break;
        case specification_1.DataType.Image:
            kinds = [specification_1.DataKind.Categorical];
            break;
        case specification_1.DataType.Number:
            kinds = [specification_1.DataKind.Categorical, specification_1.DataKind.Numerical];
            break;
    }
    return kinds;
}
exports.getConvertableDataKind = getConvertableDataKind;
function getPreferredDataKind(type) {
    var kind;
    switch (type) {
        case specification_1.DataType.Boolean:
            kind = specification_1.DataKind.Categorical;
            break;
        case specification_1.DataType.Date:
            kind = specification_1.DataKind.Temporal;
            break;
        case specification_1.DataType.String:
            kind = specification_1.DataKind.Categorical;
            break;
        case specification_1.DataType.Image:
            kind = specification_1.DataKind.Categorical;
            break;
        case specification_1.DataType.Number:
            kind = specification_1.DataKind.Numerical;
            break;
    }
    return kind;
}
exports.getPreferredDataKind = getPreferredDataKind;
function getConvertableTypes(type, dataSample) {
    var types;
    switch (type) {
        case specification_1.DataType.Boolean:
            types = [specification_1.DataType.Number, specification_1.DataType.String, specification_1.DataType.Boolean];
            break;
        case specification_1.DataType.Date:
            types = [specification_1.DataType.Number, specification_1.DataType.String, specification_1.DataType.Date];
            break;
        case specification_1.DataType.String:
            types = [
                specification_1.DataType.Number,
                specification_1.DataType.String,
                specification_1.DataType.Boolean,
                specification_1.DataType.Date,
                specification_1.DataType.Image,
            ];
            break;
        case specification_1.DataType.Number:
            types = [
                specification_1.DataType.Number,
                specification_1.DataType.String,
                specification_1.DataType.Boolean,
                specification_1.DataType.Date,
            ];
            break;
        case specification_1.DataType.Image:
            types = [specification_1.DataType.Image, specification_1.DataType.String];
            break;
    }
    return types.filter(function (t) {
        if (t == type) {
            return true;
        }
        if (dataSample) {
            return checkConvertion(t, dataSample.map(function (d) { return d && d.toString(); }));
        }
    });
}
exports.getConvertableTypes = getConvertableTypes;
/** Fill table with values converted to @param type from origin table */
function convertColumns(table, column, originTable, type) {
    var applyConvertedValues = function (table, columnName, convertedValues) {
        table.rows.forEach(function (value, index) {
            value[columnName] = convertedValues[index];
        });
    };
    var originColumn = originTable.columns.find(function (col) { return col.name === column.name; });
    var columnValues = originTable.rows.map(function (row) { return row[column.metadata.rawColumnName] || row[column.name]; });
    var typeBeforeChange = column.type;
    column.type = type;
    columnValues = originTable.rows.map(function (row) {
        var value = row[column.metadata.rawColumnName] || row[column.name];
        return value && value.toString();
    });
    try {
        var convertedValues = data_types_1.convertColumn(type, columnValues, table.localeNumberFormat, new Date().getTimezoneOffset() // time zone offset in minutes
        );
        if (convertedValues.filter(function (val) { return val; }).length === 0) {
            throw Error("Converting column type from " + originColumn.type + " to " + type + " failed");
        }
        applyConvertedValues(table, column.name, convertedValues);
        return null;
    }
    catch (ex) {
        var messgae = "Converting column type from " + originColumn.type + " to " + type + " failed";
        console.warn(messgae);
        // rollback type
        column.type = typeBeforeChange;
        return messgae;
    }
}
exports.convertColumns = convertColumns;
function copyToClipboard(str) {
    var el = document.createElement("textarea");
    el.value = str;
    document.body.appendChild(el);
    el.select();
    document.execCommand("copy");
    document.body.removeChild(el);
}
exports.copyToClipboard = copyToClipboard;
function isInIFrame() {
    try {
        return window.self !== window.top;
    }
    catch (ex) {
        return true;
    }
}
exports.isInIFrame = isInIFrame;
function getAligntment(anchor) {
    var alignX;
    var avgPopupWindowWidth = 500;
    var anchorCloseToWindowBorder = window.innerWidth - anchor.getBoundingClientRect().x < avgPopupWindowWidth;
    var alignLeft = false;
    if (anchorCloseToWindowBorder) {
        alignX = "end-inner";
        alignLeft = true;
    }
    else {
        alignX = "end-outer";
        alignLeft = false;
    }
    return { alignLeft: alignLeft, alignX: alignX };
}
exports.getAligntment = getAligntment;
/** Test if a deep equals b with tolerance on numeric values */
function expect_deep_approximately_equals(a, b, tol, weak) {
    var e_4, _a;
    if (weak === void 0) { weak = false; }
    if (weak && a == null && b == null) {
        return;
    }
    else if (a == null || b == null) {
        // If either of a, b is null/undefined
        chai_1.expect(a).equals(b);
    }
    else if (typeof a == "object" && typeof b == "object") {
        if (a instanceof Array && b instanceof Array) {
            // Both are arrays, recursively test for each item in the arrays
            chai_1.expect(a.length).to.equals(b.length);
            for (var i = 0; i < a.length; i++) {
                expect_deep_approximately_equals(a[i], b[i], tol, weak);
            }
        }
        else if (a instanceof Array || b instanceof Array) {
            // One of them is an array, the other one isn't, error
            throw new Error("type mismatch");
        }
        else {
            // Both are objects, recursively test for each key in the objects
            var keysA = Object.keys(a).sort();
            var keysB = Object.keys(b).sort();
            chai_1.expect(keysA).to.deep.equals(keysB);
            try {
                for (var keysA_1 = __values(keysA), keysA_1_1 = keysA_1.next(); !keysA_1_1.done; keysA_1_1 = keysA_1.next()) {
                    var key = keysA_1_1.value;
                    expect_deep_approximately_equals(a[key], b[key], tol, weak);
                }
            }
            catch (e_4_1) { e_4 = { error: e_4_1 }; }
            finally {
                try {
                    if (keysA_1_1 && !keysA_1_1.done && (_a = keysA_1.return)) _a.call(keysA_1);
                }
                finally { if (e_4) throw e_4.error; }
            }
        }
    }
    else {
        if (typeof a == "number" && typeof b == "number") {
            // If both are numbers, test approximately equals
            chai_1.expect(a).to.approximately(b, tol);
        }
        else {
            // Otherwise, use regular equals
            chai_1.expect(a).equals(b);
        }
    }
}
exports.expect_deep_approximately_equals = expect_deep_approximately_equals;
function replaceUndefinedByNull(value) {
    return value === undefined ? null : value;
}
exports.replaceUndefinedByNull = replaceUndefinedByNull;
//# sourceMappingURL=index.js.map