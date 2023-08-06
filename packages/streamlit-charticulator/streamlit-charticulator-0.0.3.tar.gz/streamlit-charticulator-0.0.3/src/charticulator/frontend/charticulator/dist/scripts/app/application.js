"use strict";
/* eslint-disable max-lines-per-function */
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
/* eslint-disable max-lines-per-function */
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
exports.Application = exports.NestedEditorEventType = exports.ApplicationExtensionContext = void 0;
var React = require("react");
var ReactDOM = require("react-dom");
var main_view_1 = require("./main_view");
var stores_1 = require("./stores");
var core_1 = require("../core");
var worker_1 = require("../worker");
var utils_1 = require("./utils");
var actions_1 = require("./actions");
var file_view_1 = require("./views/file_view");
var default_dataset_1 = require("./default_dataset");
var strings_1 = require("../strings");
var globals_1 = require("./globals");
// Also available from @uifabric/icons (7 and earlier) and @fluentui/font-icons-mdl2 (8+)
var index_1 = require("../fabric-icons/src/index");
index_1.initializeIcons();
var defaults_1 = require("./stores/defaults");
var specification_1 = require("../core/specification");
var app_store_1 = require("./stores/app_store");
var ApplicationExtensionContext = /** @class */ (function () {
    function ApplicationExtensionContext(app) {
        this.app = app;
    }
    ApplicationExtensionContext.prototype.getGlobalDispatcher = function () {
        return this.app.appStore.dispatcher;
    };
    /** Get the store */
    ApplicationExtensionContext.prototype.getAppStore = function () {
        return this.app.appStore;
    };
    ApplicationExtensionContext.prototype.getApplication = function () {
        return this.app;
    };
    return ApplicationExtensionContext;
}());
exports.ApplicationExtensionContext = ApplicationExtensionContext;
var NestedEditorEventType;
(function (NestedEditorEventType) {
    NestedEditorEventType["Load"] = "load";
    NestedEditorEventType["Save"] = "save";
})(NestedEditorEventType = exports.NestedEditorEventType || (exports.NestedEditorEventType = {}));
var Application = /** @class */ (function () {
    function Application() {
    }
    Application.prototype.destroy = function () {
        ReactDOM.unmountComponentAtNode(document.getElementById(this.containerID));
    };
    Application.prototype.initialize = function (config, containerID, workerConfig, localizaiton, utcTimeZone, handlers) {
        var _a, _b, _c;
        return __awaiter(this, void 0, void 0, function () {
            var UtcTimeZone, CurrencySymbol, DelimiterSymbol, GroupSymbol, NumberFormatRemove;
            var _this = this;
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        this.config = config;
                        this.containerID = containerID;
                        return [4 /*yield*/, core_1.initialize(config)];
                    case 1:
                        _d.sent();
                        if (workerConfig.worker) {
                            this.worker = workerConfig.worker;
                        }
                        else {
                            this.worker = new worker_1.CharticulatorWorker(workerConfig.workerScriptContent);
                        }
                        return [4 /*yield*/, this.worker.initialize(config)];
                    case 2:
                        _d.sent();
                        this.appStore = new stores_1.AppStore(this.worker, default_dataset_1.makeDefaultDataset());
                        if (handlers === null || handlers === void 0 ? void 0 : handlers.nestedEditor) {
                            this.nestedEditor = handlers === null || handlers === void 0 ? void 0 : handlers.nestedEditor;
                            if (handlers === null || handlers === void 0 ? void 0 : handlers.nestedEditor.onOpenEditor) {
                                this.appStore.addListener(stores_1.AppStore.EVENT_OPEN_NESTED_EDITOR, function (options, object, property) {
                                    _this.nestedEditor.onOpenEditor(options, object, property);
                                });
                            }
                        }
                        try {
                            UtcTimeZone = core_1.parseSafe(window.localStorage.getItem(globals_1.LocalStorageKeys.UtcTimeZone), true);
                            CurrencySymbol = core_1.parseSafe(window.localStorage.getItem(globals_1.LocalStorageKeys.CurrencySymbol), core_1.defaultCurrency);
                            DelimiterSymbol = core_1.parseSafe(window.localStorage.getItem(globals_1.LocalStorageKeys.DelimiterSymbol) ||
                                core_1.defaultDelimiter, core_1.defaultDelimiter);
                            GroupSymbol = core_1.parseSafe(window.localStorage.getItem(globals_1.LocalStorageKeys.GroupSymbol), core_1.defaultDigitsGroup);
                            NumberFormatRemove = core_1.parseSafe(window.localStorage.getItem(globals_1.LocalStorageKeys.NumberFormatRemove) ||
                                core_1.defaultNumberFormat.remove, core_1.defaultNumberFormat.remove);
                            this.appStore.setLocaleFileFormat({
                                currency: core_1.parseSafe(CurrencySymbol, core_1.defaultCurrency),
                                delimiter: DelimiterSymbol,
                                group: core_1.parseSafe(GroupSymbol, core_1.defaultDigitsGroup),
                                numberFormat: {
                                    decimal: NumberFormatRemove === "," ? "." : ",",
                                    remove: NumberFormatRemove === "," ? "," : ".",
                                },
                                utcTimeZone: utcTimeZone !== undefined ? utcTimeZone : UtcTimeZone,
                            });
                            core_1.setFormatOptions({
                                currency: core_1.parseSafe(CurrencySymbol, core_1.defaultCurrency),
                                grouping: core_1.parseSafe(GroupSymbol, core_1.defaultDigitsGroup),
                                decimal: NumberFormatRemove === "," ? "." : ",",
                                thousands: NumberFormatRemove === "," ? "," : ".",
                            });
                            core_1.setTimeZone(utcTimeZone !== undefined ? utcTimeZone : UtcTimeZone);
                        }
                        catch (ex) {
                            core_1.setFormatOptions({
                                currency: (_a = [localizaiton === null || localizaiton === void 0 ? void 0 : localizaiton.currency, ""]) !== null && _a !== void 0 ? _a : core_1.defaultCurrency,
                                grouping: core_1.defaultDigitsGroup,
                                decimal: (_b = localizaiton === null || localizaiton === void 0 ? void 0 : localizaiton.decemalDelimiter) !== null && _b !== void 0 ? _b : core_1.defaultNumberFormat.decimal,
                                thousands: (_c = localizaiton === null || localizaiton === void 0 ? void 0 : localizaiton.thousandsDelimiter) !== null && _c !== void 0 ? _c : core_1.defaultNumberFormat.decimal,
                            });
                            console.warn("Loadin localization settings failed");
                        }
                        window.mainStore = this.appStore;
                        ReactDOM.render(React.createElement(main_view_1.MainView, { store: this.appStore, ref: function (e) { return (_this.mainView = e); }, viewConfiguration: this.config.MainView, menuBarHandlers: handlers === null || handlers === void 0 ? void 0 : handlers.menuBarHandlers, tabButtons: handlers === null || handlers === void 0 ? void 0 : handlers.tabButtons, telemetry: handlers === null || handlers === void 0 ? void 0 : handlers.telemetry }), document.getElementById(containerID));
                        this.extensionContext = new ApplicationExtensionContext(this);
                        // Load extensions if any
                        if (config.Extensions) {
                            config.Extensions.forEach(function (ext) {
                                var scriptTag = document.createElement("script");
                                if (typeof ext.script == "string") {
                                    scriptTag.src = ext.script;
                                }
                                else {
                                    scriptTag.integrity = ext.script.integrity;
                                    scriptTag.src = ext.script.src + "?sha256=" + ext.script.sha256;
                                }
                                scriptTag.onload = function () {
                                    // An extension may include script for its initialization
                                    var initFn = new Function("application", ext.initialize);
                                    initFn(_this);
                                };
                                document.body.appendChild(scriptTag);
                            });
                        }
                        return [4 /*yield*/, this.processHashString()];
                    case 3:
                        _d.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    // eslint-disable-next-line
    Application.prototype.setupNestedEditor = function (id, onInitialized, onSave, onClose, editorMode) {
        var _this = this;
        var appStore = this.appStore;
        var setupCallback = (function (data) {
            var _a;
            var info = data;
            info.specification.mappings.width = {
                type: specification_1.MappingType.value,
                value: info.width,
            };
            info.specification.mappings.height = {
                type: specification_1.MappingType.value,
                value: info.height,
            };
            var chartManager = new core_1.Prototypes.ChartStateManager(info.specification, info.dataset, null, {}, {}, core_1.deepClone(info.specification));
            // if version wasn't saved in tempalte we asume it is 2.0.3
            if (info.template && info.template.version == undefined) {
                info.template.version = defaults_1.defaultVersionOfTemplate;
            }
            var newState = new stores_1.Migrator().migrate({
                chart: chartManager.chart,
                chartState: chartManager.chartState,
                dataset: chartManager.dataset,
                version: ((_a = info.template) === null || _a === void 0 ? void 0 : _a.version) || defaults_1.defaultVersionOfTemplate,
                originDataset: appStore.originDataset,
            }, CHARTICULATOR_PACKAGE.version);
            appStore.dispatcher.dispatch(new actions_1.Actions.ImportChartAndDataset(info.specification, info.dataset, {
                filterCondition: info.filterCondition,
            }, info.originSpecification));
            if (info.template) {
                info.template.version = newState.version;
            }
            if (onClose) {
                appStore.addListener(stores_1.AppStore.EVENT_NESTED_EDITOR_CLOSE, function () {
                    onClose();
                });
            }
            var type = _this.config.CorsPolicy && _this.config.CorsPolicy.Embedded
                ? app_store_1.EditorType.Embedded
                : app_store_1.EditorType.Nested;
            // settings from outside overrides the configuration
            if (editorMode) {
                type = editorMode;
            }
            appStore.setupNestedEditor(function (newSpecification) {
                var template = core_1.deepClone(appStore.buildChartTemplate());
                if (window.opener) {
                    window.opener.postMessage({
                        id: id,
                        type: "save" /* Save */,
                        specification: newSpecification,
                        template: template,
                    }, document.location.origin);
                }
                else {
                    if (_this.config.CorsPolicy && _this.config.CorsPolicy.TargetOrigins) {
                        window.parent.postMessage({
                            id: id,
                            type: "save" /* Save */,
                            specification: newSpecification,
                            template: template,
                        }, _this.config.CorsPolicy.TargetOrigins);
                    }
                    if ((_this.config.CorsPolicy && _this.config.CorsPolicy.Embedded) ||
                        onSave) {
                        onSave({
                            specification: newSpecification,
                            template: template,
                        });
                    }
                }
            }, type);
        }).bind(this);
        window.addEventListener("message", function (e) {
            if (e.data.id != id) {
                return;
            }
            setupCallback(e.data);
        });
        if (window.opener) {
            window.opener.postMessage({
                id: id,
                type: "initialized" /* Initialized */,
            }, document.location.origin);
        }
        else {
            if (this.config.CorsPolicy && this.config.CorsPolicy.TargetOrigins) {
                window.parent.postMessage({
                    id: id,
                    type: "initialized" /* Initialized */,
                }, this.config.CorsPolicy.TargetOrigins);
            }
            else if ((this.config.CorsPolicy &&
                this.config.CorsPolicy.Embedded &&
                onInitialized) ||
                onInitialized) {
                onInitialized(id, function (data) {
                    setupCallback(data);
                });
            }
        }
    };
    Application.prototype.processHashString = function () {
        return __awaiter(this, void 0, void 0, function () {
            var hashParsed, spec, loader, dataset, localeFileFormat_1, spec, loader, dataset, value, json;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        hashParsed = utils_1.parseHashString(document.location.hash);
                        if (!hashParsed.nestedEditor) return [3 /*break*/, 1];
                        document.title = strings_1.strings.app.nestedChartTitle;
                        this.setupNestedEditor(hashParsed.nestedEditor);
                        return [3 /*break*/, 9];
                    case 1:
                        if (!hashParsed.loadDataset) return [3 /*break*/, 3];
                        spec = JSON.parse(hashParsed.dataset);
                        loader = new core_1.Dataset.DatasetLoader();
                        return [4 /*yield*/, loader.loadDatasetFromSourceSpecification(spec)];
                    case 2:
                        dataset = _a.sent();
                        this.appStore.dispatcher.dispatch(new actions_1.Actions.ImportDataset(dataset));
                        return [3 /*break*/, 9];
                    case 3:
                        if (!hashParsed.loadCSV) return [3 /*break*/, 5];
                        localeFileFormat_1 = {
                            delimiter: core_1.defaultDelimiter,
                            numberFormat: core_1.defaultNumberFormat,
                            currency: null,
                            group: null,
                            utcTimeZone: true,
                        };
                        spec = {
                            tables: hashParsed.loadCSV
                                .split("|")
                                .map(function (x) { return ({ url: x, localeFileFormat: localeFileFormat_1 }); }),
                        };
                        loader = new core_1.Dataset.DatasetLoader();
                        return [4 /*yield*/, loader.loadDatasetFromSourceSpecification(spec)];
                    case 4:
                        dataset = _a.sent();
                        this.appStore.dispatcher.dispatch(new actions_1.Actions.ImportDataset(dataset));
                        return [3 /*break*/, 9];
                    case 5:
                        if (!hashParsed.load) return [3 /*break*/, 8];
                        return [4 /*yield*/, fetch(hashParsed.load)];
                    case 6:
                        value = _a.sent();
                        return [4 /*yield*/, value.json()];
                    case 7:
                        json = _a.sent();
                        this.appStore.dispatcher.dispatch(new actions_1.Actions.Load(json.state));
                        return [3 /*break*/, 9];
                    case 8:
                        this.mainView.refMenuBar.showFileModalWindow(file_view_1.MainTabs.new);
                        _a.label = 9;
                    case 9: return [2 /*return*/];
                }
            });
        });
    };
    Application.prototype.addExtension = function (extension) {
        extension.activate(this.extensionContext);
    };
    Application.prototype.registerExportTemplateTarget = function (name, ctor) {
        this.appStore.registerExportTemplateTarget(name, ctor);
    };
    Application.prototype.unregisterExportTemplateTarget = function (name) {
        this.appStore.unregisterExportTemplateTarget(name);
    };
    return Application;
}());
exports.Application = Application;
//# sourceMappingURL=application.js.map