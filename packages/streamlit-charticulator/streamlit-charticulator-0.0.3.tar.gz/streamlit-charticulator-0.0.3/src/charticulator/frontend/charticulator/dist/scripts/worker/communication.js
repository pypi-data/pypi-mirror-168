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
var __spread = (this && this.__spread) || function () {
    for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
    return ar;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.WorkerHostProcess = exports.WorkerRPC = void 0;
/**
 * The page side of the work instance, handles RPC and Tasks
 */
var WorkerRPC = /** @class */ (function () {
    function WorkerRPC(workerScriptURL) {
        var _this = this;
        this.currentUniqueID = 0;
        this.idCallbacks = new Map();
        this.worker = new Worker(workerScriptURL);
        this.worker.onmessage = function (event) {
            var msg = event.data;
            if (_this.idCallbacks.has(msg.instanceID)) {
                _this.idCallbacks.get(msg.instanceID)(msg);
            }
        };
    }
    WorkerRPC.prototype.newUniqueID = function () {
        this.currentUniqueID += 1;
        return "ID" + this.currentUniqueID;
    };
    WorkerRPC.prototype.rpc = function (path) {
        var _this = this;
        var args = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            args[_i - 1] = arguments[_i];
        }
        return new Promise(function (resolve, reject) {
            var msgID = _this.newUniqueID();
            _this.idCallbacks.set(msgID, function (message) {
                if (message.type == "rpc-result") {
                    _this.idCallbacks.delete(msgID);
                    resolve(message.returnValue);
                }
                if (message.type == "rpc-error") {
                    _this.idCallbacks.delete(msgID);
                    reject(new Error(message.errorMessage));
                }
            });
            _this.worker.postMessage({
                type: "rpc-call",
                instanceID: msgID,
                path: path,
                args: args,
            });
        });
    };
    return WorkerRPC;
}());
exports.WorkerRPC = WorkerRPC;
var WorkerHostProcess = /** @class */ (function () {
    function WorkerHostProcess() {
        var _this = this;
        this.rpcMethods = new Map();
        onmessage = function (event) {
            var message = event.data;
            _this.handleMessage(message);
        };
    }
    WorkerHostProcess.prototype.registerRPC = function (path, method) {
        this.rpcMethods.set(path, method);
    };
    WorkerHostProcess.prototype.handleMessage = function (message) {
        switch (message.type) {
            case "rpc-call":
                {
                    try {
                        var method = this.rpcMethods.get(message.path);
                        if (!method) {
                            postMessage({
                                type: "rpc-error",
                                instanceID: message.instanceID,
                                errorMessage: "RPC method \"" + message.path + "\" not found",
                            }, undefined);
                        }
                        else {
                            var result = method.apply(void 0, __spread(message.args));
                            if (result instanceof Promise) {
                                result
                                    .then(function (returnValue) {
                                    postMessage({
                                        type: "rpc-result",
                                        instanceID: message.instanceID,
                                        returnValue: returnValue,
                                    }, undefined);
                                })
                                    .catch(function (error) {
                                    postMessage({
                                        type: "rpc-error",
                                        instanceID: message.instanceID,
                                        errorMessage: error.message + "\n" + error.stack,
                                    }, undefined);
                                });
                            }
                            else {
                                postMessage({
                                    type: "rpc-result",
                                    instanceID: message.instanceID,
                                    returnValue: result,
                                }, undefined);
                            }
                        }
                    }
                    catch (e) {
                        postMessage({
                            type: "rpc-error",
                            instanceID: message.instanceID,
                            errorMessage: e.message + "\n" + e.stack,
                        }, undefined);
                    }
                }
                break;
        }
    };
    return WorkerHostProcess;
}());
exports.WorkerHostProcess = WorkerHostProcess;
//# sourceMappingURL=communication.js.map