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
exports.FileViewOpen = void 0;
var FileSaver = require("file-saver");
var React = require("react");
var R = require("../../resources");
var components_1 = require("../../components");
var actions_1 = require("../../actions");
var utils_1 = require("../../utils");
var strings_1 = require("../../../strings");
var react_1 = require("@fluentui/react");
var core_1 = require("../../../core");
var FileViewOpen = /** @class */ (function (_super) {
    __extends(FileViewOpen, _super);
    function FileViewOpen() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            chartList: [],
            chartCount: 0,
        };
        return _this;
    }
    FileViewOpen.prototype.componentDidMount = function () {
        this.updateChartList();
    };
    FileViewOpen.prototype.updateChartList = function () {
        var _this = this;
        var store = this.props.store;
        store.backend.list("chart", "timeCreated", 0, 1000).then(function (result) {
            _this.setState({
                chartList: result.items,
                chartCount: result.totalCount,
            });
        });
    };
    // eslint-disable-next-line
    FileViewOpen.prototype.renderChartList = function () {
        var _this = this;
        var store = this.props.store;
        var backend = store.backend;
        if (this.state.chartList == null) {
            return (React.createElement("p", { className: "loading-indicator" },
                React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon("loading") }),
                " ",
                strings_1.strings.app.loading));
        }
        else {
            if (this.state.chartCount == 0) {
                return React.createElement("p", null, strings_1.strings.fileOpen.noChart);
            }
            else {
                return (React.createElement("ul", { className: "chart-list" }, this.state.chartList.map(function (chart) {
                    return (React.createElement("li", { key: chart.id, tabIndex: 0, onClick: function () {
                            _this.props.store.dispatcher.dispatch(new actions_1.Actions.Open(chart.id, function (error) {
                                if (error) {
                                    // TODO: add error reporting
                                }
                                else {
                                    _this.props.onClose();
                                }
                            }));
                        }, onKeyPress: function (e) {
                            if (e.key === "Enter") {
                                _this.props.store.dispatcher.dispatch(new actions_1.Actions.Open(chart.id, function (error) {
                                    if (error) {
                                        // TODO: add error reporting
                                    }
                                    else {
                                        _this.props.onClose();
                                    }
                                }));
                            }
                        } },
                        React.createElement("div", { className: "thumbnail" },
                            React.createElement("img", { src: chart.metadata.thumbnail })),
                        React.createElement("div", { className: "description" },
                            React.createElement("div", { className: "name", onClick: function (e) { return e.stopPropagation(); } },
                                React.createElement(components_1.EditableTextView, { text: chart.metadata.name, onEdit: function (newText) {
                                        backend.get(chart.id).then(function (chart) {
                                            chart.metadata.name = newText;
                                            backend
                                                .put(chart.id, chart.data, chart.metadata)
                                                .then(function () {
                                                _this.updateChartList();
                                            });
                                        });
                                    } })),
                            React.createElement("div", { className: "metadata" }, chart.metadata.dataset),
                            React.createElement("div", { className: "footer" },
                                React.createElement("div", { className: "metadata" }, new Date(chart.metadata.timeCreated).toLocaleString()),
                                React.createElement("div", { className: "actions" },
                                    React.createElement(components_1.ButtonFlat, { url: R.getSVGIcon("toolbar/trash"), title: strings_1.strings.fileOpen.delete, stopPropagation: true, onClick: function () {
                                            if (confirm(strings_1.strings.fileOpen.deleteConfirmation(chart.metadata.name))) {
                                                backend.delete(chart.id).then(function () {
                                                    _this.updateChartList();
                                                });
                                            }
                                        } }),
                                    React.createElement(components_1.ButtonFlat, { url: R.getSVGIcon("toolbar/copy"), title: strings_1.strings.fileOpen.copy, stopPropagation: true, onClick: function () {
                                            backend.get(chart.id).then(function (chart) {
                                                backend
                                                    .create("chart", chart.data, chart.metadata)
                                                    .then(function () {
                                                    _this.updateChartList();
                                                });
                                            });
                                        } }),
                                    React.createElement(components_1.ButtonFlat, { url: R.getSVGIcon("toolbar/download"), title: strings_1.strings.fileOpen.download, stopPropagation: true, onClick: function () {
                                            backend.get(chart.id).then(function (chart) {
                                                var blob = new Blob([
                                                    JSON.stringify(chart.data, null, 2),
                                                ]);
                                                FileSaver.saveAs(blob, chart.metadata.name.replace(
                                                // eslint-disable-next-line
                                                /[^0-9a-zA-Z\ \.\-\_]+/g, "_") + ".chart");
                                            });
                                        } }))))));
                })));
            }
        }
    };
    FileViewOpen.prototype.render = function () {
        var _this = this;
        return (React.createElement("section", { className: "charticulator__file-view-content is-fix-width" },
            React.createElement("h1", null, strings_1.strings.mainTabs.open),
            React.createElement("div", { style: { marginBottom: "12px" } },
                React.createElement(react_1.DefaultButton, { iconProps: {
                        iconName: "OpenFolderHorizontal",
                    }, styles: core_1.primaryButtonStyles, text: strings_1.strings.fileOpen.open, onClick: function () { return __awaiter(_this, void 0, void 0, function () {
                        var file, str, data;
                        return __generator(this, function (_a) {
                            switch (_a.label) {
                                case 0: return [4 /*yield*/, utils_1.showOpenFileDialog(["chart"])];
                                case 1:
                                    file = _a.sent();
                                    return [4 /*yield*/, utils_1.readFileAsString(file)];
                                case 2:
                                    str = _a.sent();
                                    data = JSON.parse(str);
                                    this.props.store.dispatcher.dispatch(new actions_1.Actions.Load(data.state));
                                    this.props.onClose();
                                    return [2 /*return*/];
                            }
                        });
                    }); } })),
            this.renderChartList()));
    };
    return FileViewOpen;
}(React.Component));
exports.FileViewOpen = FileViewOpen;
//# sourceMappingURL=open_view.js.map