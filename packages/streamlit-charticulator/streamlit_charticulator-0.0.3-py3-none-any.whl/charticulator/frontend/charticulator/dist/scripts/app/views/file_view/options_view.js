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
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
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
exports.FileViewOptions = exports.FileViewOptionsView = void 0;
var React = require("react");
var react_1 = require("react");
var common_1 = require("../../../core/common");
var strings_1 = require("../../../strings");
var context_component_1 = require("../../context_component");
var globals_1 = require("../../globals");
var hooks_1 = require("../../utils/hooks");
// eslint-disable-next-line
exports.FileViewOptionsView = function () {
    var store = react_1.useContext(context_component_1.MainReactContext).store;
    var localeFileFormat = store.getLocaleFileFormat();
    var _a = __read(hooks_1.useLocalStorage(localeFileFormat.numberFormat.remove, globals_1.LocalStorageKeys.NumberFormatRemove), 2), numberFormatRemove = _a[0], setNumberFormatRemove = _a[1];
    var _b = __read(hooks_1.useLocalStorage(localeFileFormat.delimiter, globals_1.LocalStorageKeys.DelimiterSymbol), 2), delimiterSymbol = _b[0], setDelimiterSymbol = _b[1];
    var _c = __read(hooks_1.useLocalStorage(localeFileFormat.utcTimeZone, globals_1.LocalStorageKeys.UtcTimeZone), 2), utcTimeZone = _c[0], setUtcTimeZone = _c[1];
    // const [currencySymbol, setCurrencySymbol] = useLocalStorage<string>(
    //   localeFileFormat.currency,
    //   LocalStorageKeys.CurrencySymbol
    // );
    // const [groupSymbol, setGroupSymbol] = useLocalStorage<string>(
    //   localeFileFormat.group,
    //   LocalStorageKeys.GroupSymbol
    // );
    var changeLocaleFileFormat = function (localeFileFormat) {
        store.setLocaleFileFormat(localeFileFormat);
        store.solveConstraintsAndUpdateGraphics();
    };
    return (React.createElement("section", { className: "charticulator__file-view-content" },
        React.createElement("h1", null, strings_1.strings.mainTabs.options),
        React.createElement("div", null,
            React.createElement("h2", null, strings_1.strings.options.fileFormat),
            React.createElement("div", null,
                React.createElement("div", { className: "form-group" },
                    React.createElement("select", { onChange: function (e) {
                            changeLocaleFileFormat(__assign(__assign({}, localeFileFormat), { delimiter: e.target.options[e.target.selectedIndex].value }));
                            setDelimiterSymbol(e.target.options[e.target.selectedIndex].value);
                        }, value: delimiterSymbol },
                        React.createElement("option", { value: "," }, strings_1.strings.options.comma),
                        React.createElement("option", { value: ";" }, strings_1.strings.options.semicolon)),
                    React.createElement("label", null, strings_1.strings.options.delimiter)),
                React.createElement("div", { className: "form-group" },
                    React.createElement("select", { onChange: function (e) {
                            var isDecimalDot = e.target.options[e.target.selectedIndex].value === ","; // values is removeal
                            changeLocaleFileFormat(__assign(__assign({}, localeFileFormat), { numberFormat: {
                                    decimal: isDecimalDot ? "." : ",",
                                    remove: isDecimalDot ? "," : ".",
                                } }));
                            setNumberFormatRemove(isDecimalDot ? "," : ".");
                            common_1.setFormatOptions({
                                decimal: isDecimalDot ? "." : ",",
                                thousands: isDecimalDot ? "," : ".",
                                currency: common_1.parseSafe(localeFileFormat.currency, common_1.defaultCurrency),
                                grouping: common_1.parseSafe(localeFileFormat.group, common_1.defaultDigitsGroup),
                            });
                        }, value: numberFormatRemove },
                        React.createElement("option", { value: "," }, strings_1.strings.options.numberFormatDot),
                        React.createElement("option", { value: "." }, strings_1.strings.options.numberFormatComma)),
                    React.createElement("label", null, strings_1.strings.options.numberFormat)),
                React.createElement("div", { className: "form-group" },
                    React.createElement("select", { onChange: function (e) {
                            changeLocaleFileFormat(__assign(__assign({}, localeFileFormat), { utcTimeZone: e.target.options[e.target.selectedIndex].value === "true" }));
                            setUtcTimeZone(e.target.options[e.target.selectedIndex].value === "true");
                            common_1.setTimeZone(e.target.options[e.target.selectedIndex].value === "true");
                        }, value: utcTimeZone ? "true" : "false" },
                        React.createElement("option", { value: "true" }, strings_1.strings.options.utc),
                        React.createElement("option", { value: "false" }, strings_1.strings.options.local)),
                    React.createElement("label", null, strings_1.strings.options.timeZone))))));
};
// TODO create HOC
var FileViewOptions = /** @class */ (function (_super) {
    __extends(FileViewOptions, _super);
    function FileViewOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    FileViewOptions.prototype.render = function () {
        return (React.createElement(exports.FileViewOptionsView, { onClose: this.props.onClose }));
    };
    return FileViewOptions;
}(React.Component));
exports.FileViewOptions = FileViewOptions;
//# sourceMappingURL=options_view.js.map