"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.objectHash = exports.uniqueID = exports.uuid = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
function s4() {
    // eslint-disable-next-line
    return Math.floor((1 + Math.random()) * 0x10000)
        .toString(16)
        .substring(1);
}
function uuid() {
    return (s4() +
        s4() +
        "-" +
        s4() +
        "-" +
        s4() +
        "-" +
        s4() +
        "-" +
        s4() +
        s4() +
        s4());
}
exports.uuid = uuid;
var usedIDs = new Set();
/** Generate a unique ID in uuid format */
function uniqueID() {
    // eslint-disable-next-line
    while (true) {
        // eslint-disable-next-line
        var id = Math.random().toString(36).substr(2);
        if (!usedIDs.has(id)) {
            usedIDs.add(id);
            return id;
        }
    }
}
exports.uniqueID = uniqueID;
var hashIndex = 1;
var objectHashs = new WeakMap();
function objectHash(o) {
    if (objectHashs.has(o)) {
        return objectHashs.get(o);
    }
    var newHash = "<#" + hashIndex.toString() + ">";
    hashIndex += 1;
    objectHashs.set(o, newHash);
    return newHash;
}
exports.objectHash = objectHash;
//# sourceMappingURL=unique_id.js.map