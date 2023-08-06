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
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.FileView = exports.CurrentChartView = exports.MainTabs = void 0;
/**
 * Components to save, open, create, export charts.
 *
 * ![File view](media://file_view.png)
 *
 * * {@link "app/views/file_view/new_view"} / {@link "app/views/file_view/import_data_view"} - component with two file inputs for main table data and links table data
 *
 * ![File view](media://file_view_new.png)
 *
 * * {@link "app/views/file_view/open_view"}
 *
 * ![File view](media://file_view_open.png)
 *
 * * {@link "app/views/file_view/save_view"}
 *
 * ![File view](media://file_view_save.png)
 *
 * * {@link "app/views/file_view/export_view"}
 *
 * ![File view](media://file_view_export.png)
 *
 * @packageDocumentation
 * @preferred
 */
var React = require("react");
var R = require("../../resources");
var components_1 = require("../../components");
var utils_1 = require("../../utils");
var export_view_1 = require("./export_view");
var new_view_1 = require("./new_view");
var open_view_1 = require("./open_view");
var save_view_1 = require("./save_view");
var options_view_1 = require("./options_view");
var strings_1 = require("../../../strings");
var context_component_1 = require("../../context_component");
var MainTabs;
(function (MainTabs) {
    MainTabs["about"] = "about";
    MainTabs["export"] = "export";
    MainTabs["new"] = "new";
    MainTabs["open"] = "open";
    MainTabs["options"] = "options";
    MainTabs["save"] = "save";
})(MainTabs = exports.MainTabs || (exports.MainTabs = {}));
var tabOrder = [
    MainTabs.new,
    MainTabs.open,
    MainTabs.save,
    MainTabs.export,
    MainTabs.options,
    null,
    MainTabs.about,
];
var CurrentChartView = /** @class */ (function (_super) {
    __extends(CurrentChartView, _super);
    function CurrentChartView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            svgDataURL: null,
        };
        _this.renderImage();
        return _this;
    }
    CurrentChartView.prototype.renderImage = function () {
        return __awaiter(this, void 0, void 0, function () {
            var svg;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.props.store.renderLocalSVG()];
                    case 1:
                        svg = _a.sent();
                        this.setState({
                            svgDataURL: utils_1.stringToDataURL("image/svg+xml", svg),
                        });
                        return [2 /*return*/];
                }
            });
        });
    };
    CurrentChartView.prototype.render = function () {
        return (React.createElement("div", { className: "current-chart-view" },
            React.createElement("img", { src: this.state.svgDataURL })));
    };
    return CurrentChartView;
}(React.PureComponent));
exports.CurrentChartView = CurrentChartView;
var FileView = /** @class */ (function (_super) {
    __extends(FileView, _super);
    function FileView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            currentTab: _this.props.defaultTab || MainTabs.open,
        };
        return _this;
    }
    FileView.prototype.componentDidMount = function () {
        var _this = this;
        setTimeout(function () {
            var _a;
            (_a = _this.buttonBack) === null || _a === void 0 ? void 0 : _a.focus();
        }, 100);
    };
    FileView.prototype.switchTab = function (currentTab) {
        this.setState({ currentTab: currentTab });
    };
    FileView.prototype.renderContent = function () {
        switch (this.state.currentTab) {
            case MainTabs.new: {
                return (React.createElement(new_view_1.FileViewNew, { store: this.props.store, onClose: this.props.onClose }));
            }
            case MainTabs.save: {
                return (React.createElement(save_view_1.FileViewSaveAs, { store: this.props.store, onClose: this.props.onClose }));
            }
            case MainTabs.export: {
                return (React.createElement(export_view_1.FileViewExport, { store: this.props.store, onClose: this.props.onClose }));
            }
            case MainTabs.options: {
                return React.createElement(options_view_1.FileViewOptionsView, { onClose: this.props.onClose });
            }
            case MainTabs.about: {
                return (React.createElement("iframe", { className: "charticulator__file-view-about", src: "about.html", style: { flex: "1" } }));
            }
            case MainTabs.open:
            default: {
                return (React.createElement(open_view_1.FileViewOpen, { store: this.props.store, onClose: this.props.onClose }));
            }
        }
    };
    FileView.prototype.render = function () {
        var _this = this;
        return (React.createElement(context_component_1.MainReactContext.Provider, { value: { store: this.props.store } },
            React.createElement("div", { className: "charticulator__file-view" },
                React.createElement("div", { className: "charticulator__file-view-tabs" },
                    React.createElement("div", { ref: function (r) { return (_this.buttonBack = r); }, tabIndex: 0, className: "el-button-back", onClick: function () { return _this.props.onClose(); }, onKeyPress: function (e) {
                            if (e.key === "Enter") {
                                _this.props.onClose();
                            }
                        } },
                        React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon("toolbar/back") })),
                    tabOrder.map(function (t, index) {
                        return t === null ? (React.createElement("div", { key: index, className: "el-sep" })) : (React.createElement("div", { tabIndex: 0, key: index, className: utils_1.classNames("el-tab", [
                                "active",
                                _this.state.currentTab == t,
                            ]), onClick: function () { return _this.switchTab(t); }, onKeyPress: function (e) {
                                if (e.key === "Enter") {
                                    _this.switchTab(t);
                                }
                            } }, strings_1.strings.mainTabs[t]));
                    })),
                React.createElement(components_1.TelemetryContext.Consumer, null, function (telemetryRecorder) {
                    return (React.createElement(components_1.ErrorBoundary, { telemetryRecorder: telemetryRecorder }, _this.renderContent()));
                }))));
    };
    return FileView;
}(React.Component));
exports.FileView = FileView;
//# sourceMappingURL=index.js.map