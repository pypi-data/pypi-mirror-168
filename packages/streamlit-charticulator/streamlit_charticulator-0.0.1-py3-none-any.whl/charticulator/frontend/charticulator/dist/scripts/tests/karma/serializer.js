// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
/* tslint:disable */
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.matchSnapshot = void 0;
var utils_1 = require("../unit/utils");
var parseSync = require("svgson").parseSync;
function serialize(data) {
    return JSON.stringify(parseSync(new XMLSerializer().serializeToString(data)), null, "");
}
function snapshotPath(node) {
    var path = [];
    while (node && node.parent) {
        path.push(node.title);
        node = node.parent;
    }
    return path.reverse();
}
function matchSnapshot(chai, utils) {
    var context = window.__mocha_context__;
    var snapshotState = window.__snapshot__;
    utils.addMethod(chai.Assertion.prototype, "matchSnapshot", aMethodForExpect);
    chai.assert.matchSnapshot = aMethodForAssert;
    function aMethodForAssert(lang, msg) {
        // This basically wraps the 'expect' version of the assertion to allow using 'assert' syntax.
        return new chai.Assertion(lang, msg).to.matchSnapshot();
    }
    function aMethodForExpect(lang, update) {
        var obj = serialize(chai.util.flag(this, "object"));
        var index = context.index++;
        var path;
        // For a hook, use the currentTest for path
        if (context.runnable.type === "hook") {
            path = snapshotPath(context.runnable.ctx.currentTest);
        }
        else {
            path = snapshotPath(context.runnable);
        }
        if (update || snapshotState.update) {
            snapshotState.set(path, index, obj, lang);
        }
        else {
            var snapshot = snapshotState.get(path, index);
            if (!snapshot) {
                snapshotState.set(path, index, obj, lang);
            }
            else {
                try {
                    utils_1.expect_deep_approximately_equals(JSON.parse(obj), JSON.parse(snapshot.code), 2);
                }
                catch (ex) {
                    throw new chai.AssertionError("Received value does not match stored snapshot " + index, {
                        actual: ex.actual,
                        expected: ex.expected,
                        showDiff: true,
                        stack: ex.stack,
                    }, chai.util.flag(this, "ssfi"));
                }
            }
        }
    }
}
exports.matchSnapshot = matchSnapshot;
//# sourceMappingURL=serializer.js.map