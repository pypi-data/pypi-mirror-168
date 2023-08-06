"use strict";
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
exports.ErrorBoundary = exports.TelemetryContext = exports.TelemetryActionType = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var index_1 = require("./index");
var utils_1 = require("../utils");
var TelemetryActionType;
(function (TelemetryActionType) {
    TelemetryActionType["Exception"] = "exception";
    TelemetryActionType["ExportTemplate"] = "exportTempalte";
})(TelemetryActionType = exports.TelemetryActionType || (exports.TelemetryActionType = {}));
exports.TelemetryContext = React.createContext(null);
var ErrorBoundary = /** @class */ (function (_super) {
    __extends(ErrorBoundary, _super);
    function ErrorBoundary(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            hasError: false,
        };
        return _this;
    }
    ErrorBoundary.prototype.componentDidCatch = function (error, info) {
        var _a;
        this.setState({
            hasError: true,
            errorString: error.name + " \n " + error.message + " \n " + (error.stack && error.stack) + " \n " + info.componentStack,
        });
        (_a = this.props.telemetryRecorder) === null || _a === void 0 ? void 0 : _a.record(TelemetryActionType.Exception, {
            name: error.name,
            message: error.message,
            stack: error.stack,
        });
        console.log(error, info);
    };
    ErrorBoundary.prototype.render = function () {
        var _this = this;
        if (this.state.hasError) {
            var maxWidth = this.props.maxWidth
                ? this.props.maxWidth + "px"
                : undefined;
            return (React.createElement("div", { className: "charticulator__error-boundary-report", style: { margin: "1em", maxWidth: maxWidth } },
                React.createElement("p", null, "Oops! Something went wrong here. This must be a software bug. As a last resort, you can undo the previous change and try again."),
                React.createElement("p", null,
                    React.createElement(index_1.ButtonRaised, { text: "Try Again", onClick: function () {
                            _this.setState({
                                hasError: false,
                            });
                        } })),
                React.createElement("p", null,
                    React.createElement(index_1.ButtonRaised, { text: "Copy diagnostic information to clipboard", onClick: function () {
                            utils_1.copyToClipboard(_this.state.errorString);
                        } }))));
        }
        return this.props.children;
    };
    return ErrorBoundary;
}(React.Component));
exports.ErrorBoundary = ErrorBoundary;
//# sourceMappingURL=error_boundary.js.map