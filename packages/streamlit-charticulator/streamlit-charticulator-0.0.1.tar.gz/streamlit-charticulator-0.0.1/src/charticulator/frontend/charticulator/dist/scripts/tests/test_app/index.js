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
exports.TestApplication = exports.TestApplicationView = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var ReactDOM = require("react-dom");
var core_1 = require("../../core");
var globals_1 = require("../../app/globals");
var controllers_1 = require("../../app/controllers");
var registeredTests = [];
function registerTest(name, component) {
    registeredTests.push({ name: name, component: component });
}
var TestApplicationView = /** @class */ (function (_super) {
    __extends(TestApplicationView, _super);
    function TestApplicationView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getDefaultState();
        return _this;
    }
    TestApplicationView.prototype.getDefaultState = function () {
        var currentTest = "";
        if (document.location.hash.startsWith("#!")) {
            currentTest = document.location.hash.slice(2);
        }
        return { currentTest: currentTest };
    };
    TestApplicationView.prototype.render = function () {
        var e_1, _a;
        var _this = this;
        var TestComponent = null;
        try {
            for (var registeredTests_1 = __values(registeredTests), registeredTests_1_1 = registeredTests_1.next(); !registeredTests_1_1.done; registeredTests_1_1 = registeredTests_1.next()) {
                var c = registeredTests_1_1.value;
                if (c.name == this.state.currentTest) {
                    TestComponent = c.component;
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (registeredTests_1_1 && !registeredTests_1_1.done && (_a = registeredTests_1.return)) _a.call(registeredTests_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return (React.createElement("div", null,
            React.createElement("div", { style: {
                    padding: "10px",
                    borderBottom: "1px solid #CCC",
                    marginBottom: "10px",
                } },
                "Select Test: ",
                React.createElement("select", { value: this.state.currentTest || "", onChange: function (e) {
                        if (e.target.value == "") {
                            document.location.hash = "";
                        }
                        else {
                            document.location.hash = "#!" + e.target.value;
                        }
                        _this.setState({ currentTest: e.target.value });
                    } },
                    React.createElement("option", { value: "" }, "(no test selected)"),
                    registeredTests.map(function (test) { return (React.createElement("option", { key: test.name, value: test.name }, test.name)); }))),
            React.createElement("div", { style: { padding: "10px" } },
                TestComponent ? React.createElement(TestComponent, null) : null,
                React.createElement(controllers_1.PopupContainer, { controller: globals_1.popupController }))));
    };
    return TestApplicationView;
}(React.Component));
exports.TestApplicationView = TestApplicationView;
var TestApplication = /** @class */ (function () {
    function TestApplication() {
    }
    TestApplication.prototype.initialize = function (config, containerID) {
        return core_1.initialize(config).then(function () {
            ReactDOM.render(React.createElement(TestApplicationView, null), document.getElementById(containerID));
        });
    };
    return TestApplication;
}());
exports.TestApplication = TestApplication;
require("./graphics").register(registerTest);
require("./color_picker").register(registerTest);
//# sourceMappingURL=index.js.map