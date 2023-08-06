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
exports.ChartContainer = exports.ChartContainerEvent = exports.ChartContainerComponent = void 0;
var React = require("react");
var ReactDOM = require("react-dom");
var core_1 = require("../core");
var chart_component_1 = require("./chart_component");
var ChartContainerComponent = /** @class */ (function (_super) {
    __extends(ChartContainerComponent, _super);
    function ChartContainerComponent(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            width: _this.props.defaultWidth != null ? _this.props.defaultWidth : 900,
            height: _this.props.defaultHeight != null ? _this.props.defaultHeight : 900,
            selection: null,
            localization: null,
        };
        _this.handleGlyphClick = function (data, modifiers) {
            if (data == null) {
                _this.clearSelection(true);
            }
            else {
                _this.setSelection(data.table, data.rowIndices, modifiers.shiftKey || modifiers.ctrlKey || modifiers.metaKey, true);
            }
        };
        _this.handleGlyphContextMenuClick = function (data, modifiers) {
            if (_this.props.onMouseContextMenuClickGlyph) {
                _this.props.onMouseContextMenuClickGlyph(data, modifiers);
            }
        };
        _this.handleGlyphMouseEnter = function (data) {
            if (_this.props.onMouseEnterGlyph) {
                _this.props.onMouseEnterGlyph(data);
            }
        };
        _this.handleGlyphMouseLeave = function (data) {
            if (_this.props.onMouseLeaveGlyph) {
                _this.props.onMouseLeaveGlyph(data);
            }
        };
        return _this;
    }
    ChartContainerComponent.prototype.setSelection = function (table, rowIndices, union, emit) {
        var e_1, _a;
        if (union === void 0) { union = false; }
        if (emit === void 0) { emit = false; }
        var indicesSet = new Set(rowIndices);
        if (union && this.state.selection && this.state.selection.table == table) {
            try {
                for (var _b = __values(this.state.selection.indices), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var item = _c.value;
                    indicesSet.add(item);
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_1) throw e_1.error; }
            }
        }
        this.setState({
            selection: {
                table: table,
                indices: indicesSet,
                isSelected: function (qTable, qIndices) {
                    return (table == qTable && qIndices.find(function (v) { return indicesSet.has(v); }) >= 0);
                },
            },
        });
        if (emit && this.props.onSelectionChange) {
            this.props.onSelectionChange({
                table: table,
                rowIndices: Array.from(indicesSet),
            });
        }
    };
    ChartContainerComponent.prototype.clearSelection = function (emit) {
        if (emit === void 0) { emit = false; }
        this.setState({ selection: null });
        if (emit && this.props.onSelectionChange) {
            this.props.onSelectionChange(null);
        }
    };
    ChartContainerComponent.prototype.resize = function (width, height) {
        this.setState({ width: width, height: height });
    };
    ChartContainerComponent.prototype.getProperty = function (objectID, property) {
        return this.component.getProperty(objectID, property);
    };
    ChartContainerComponent.prototype.setProperty = function (objectID, property, value) {
        return this.component.setProperty(objectID, property, value);
    };
    ChartContainerComponent.prototype.getAttributeMapping = function (objectID, attribute) {
        return this.component.getAttributeMapping(objectID, attribute);
    };
    ChartContainerComponent.prototype.setAttributeMapping = function (objectID, attribute, mapping) {
        return this.component.setAttributeMapping(objectID, attribute, mapping);
    };
    ChartContainerComponent.prototype.render = function () {
        var _this = this;
        return (React.createElement(chart_component_1.ChartComponent, { ref: function (e) { return (_this.component = e); }, chart: this.props.chart, dataset: this.props.dataset, defaultAttributes: this.props.defaultAttributes, width: this.state.width, height: this.state.height, rootElement: "svg", selection: this.state.selection, onGlyphClick: this.handleGlyphClick, onGlyphMouseEnter: this.handleGlyphMouseEnter, onGlyphMouseLeave: this.handleGlyphMouseLeave, onGlyphContextMenuClick: this.handleGlyphContextMenuClick, renderEvents: this.props.renderEvents }));
    };
    return ChartContainerComponent;
}(React.Component));
exports.ChartContainerComponent = ChartContainerComponent;
var ChartContainerEvent;
(function (ChartContainerEvent) {
    ChartContainerEvent["Selection"] = "selection";
    ChartContainerEvent["MouseEnter"] = "mouseenter";
    ChartContainerEvent["MouseLeave"] = "mouseleave";
    ChartContainerEvent["ContextMenu"] = "contextmenu";
})(ChartContainerEvent = exports.ChartContainerEvent || (exports.ChartContainerEvent = {}));
var ChartContainer = /** @class */ (function (_super) {
    __extends(ChartContainer, _super);
    function ChartContainer(instance, dataset, renderEvents, localizaiton, utcTimeZone) {
        var _a, _b, _c;
        var _this = _super.call(this) || this;
        _this.instance = instance;
        _this.dataset = dataset;
        _this.renderEvents = renderEvents;
        _this.localizaiton = localizaiton;
        _this.utcTimeZone = utcTimeZone;
        _this.width = 1200;
        _this.height = 800;
        _this.chart = instance.chart;
        _this.defaultAttributes = instance.defaultAttributes;
        core_1.setFormatOptions({
            currency: (_a = [localizaiton === null || localizaiton === void 0 ? void 0 : localizaiton.currency, ""]) !== null && _a !== void 0 ? _a : core_1.defaultCurrency,
            grouping: core_1.defaultDigitsGroup,
            decimal: (_b = localizaiton === null || localizaiton === void 0 ? void 0 : localizaiton.decemalDelimiter) !== null && _b !== void 0 ? _b : core_1.defaultNumberFormat.decimal,
            thousands: (_c = localizaiton === null || localizaiton === void 0 ? void 0 : localizaiton.thousandsDelimiter) !== null && _c !== void 0 ? _c : core_1.defaultNumberFormat.decimal,
        });
        core_1.setTimeZone(utcTimeZone);
        return _this;
    }
    /** Resize the chart */
    ChartContainer.prototype.resize = function (width, height) {
        if (this.component) {
            this.component.resize(width, height);
        }
    };
    /** Listen to selection change */
    ChartContainer.prototype.addSelectionListener = function (listener) {
        return this.addListener(ChartContainerEvent.Selection, listener);
    };
    ChartContainer.prototype.addContextMenuListener = function (listener) {
        return this.addListener(ChartContainerEvent.ContextMenu, listener);
    };
    ChartContainer.prototype.addMouseEnterListener = function (listener) {
        return this.addListener(ChartContainerEvent.MouseEnter, listener);
    };
    ChartContainer.prototype.addMouseLeaveListener = function (listener) {
        return this.addListener(ChartContainerEvent.MouseLeave, listener);
    };
    /** Set data selection and update the chart */
    ChartContainer.prototype.setSelection = function (table, rowIndices) {
        this.component.setSelection(table, rowIndices);
    };
    /** Clear data selection and update the chart */
    ChartContainer.prototype.clearSelection = function () {
        this.component.clearSelection();
    };
    /** Get a property from the chart */
    ChartContainer.prototype.getProperty = function (objectID, property) {
        return this.component.getProperty(objectID, property);
    };
    /** Set a property to the chart */
    ChartContainer.prototype.setProperty = function (objectID, property, value) {
        return this.component.setProperty(objectID, property, value);
    };
    /**
     * Get a attribute mapping
     */
    ChartContainer.prototype.getAttributeMapping = function (objectID, attribute) {
        return this.component.getAttributeMapping(objectID, attribute);
    };
    /** Set a attribute mapping */
    ChartContainer.prototype.setAttributeMapping = function (objectID, attribute, mapping) {
        return this.component.setAttributeMapping(objectID, attribute, mapping);
    };
    ChartContainer.prototype.setChart = function (chart) {
        this.chart = chart;
        ReactDOM.render(this.reactMount(this.width, this.height), this.container);
    };
    ChartContainer.setFormatOptions = function (options) {
        core_1.setFormatOptions(options);
    };
    ChartContainer.setUtcTimeZone = function (utcTimeZone) {
        core_1.setTimeZone(utcTimeZone);
    };
    ChartContainer.prototype.reactMount = function (width, height) {
        var _this = this;
        if (width === void 0) { width = 1200; }
        if (height === void 0) { height = 800; }
        this.width = width;
        this.height = height;
        return (React.createElement(ChartContainerComponent, { ref: function (e) { return (_this.component = e); }, chart: this.chart, dataset: this.dataset, defaultWidth: width, defaultHeight: height, defaultAttributes: this.defaultAttributes, onSelectionChange: function (data) {
                if (data == null) {
                    _this.emit(ChartContainerEvent.Selection);
                }
                else {
                    _this.emit(ChartContainerEvent.Selection, data.table, data.rowIndices);
                }
            }, onMouseEnterGlyph: function (data) {
                _this.emit(ChartContainerEvent.MouseEnter, data.table, data.rowIndices);
            }, onMouseLeaveGlyph: function (data) {
                _this.emit(ChartContainerEvent.MouseLeave, data.table, data.rowIndices);
            }, onMouseContextMenuClickGlyph: function (data, modifiers) {
                _this.emit(ChartContainerEvent.ContextMenu, data.table, data.rowIndices, modifiers);
            }, renderEvents: this.renderEvents }));
    };
    /** Mount the chart to a container element */
    ChartContainer.prototype.mount = function (container, width, height) {
        if (width === void 0) { width = 1200; }
        if (height === void 0) { height = 800; }
        // We only mount in one place
        if (this.container) {
            this.unmount();
        }
        if (typeof container == "string") {
            container = document.getElementById(container);
        }
        this.container = container;
        ReactDOM.render(this.reactMount(width, height), container);
    };
    /** Unmount the chart */
    ChartContainer.prototype.unmount = function () {
        if (this.container) {
            ReactDOM.unmountComponentAtNode(this.container);
            this.container = null;
        }
    };
    return ChartContainer;
}(core_1.EventEmitter));
exports.ChartContainer = ChartContainer;
//# sourceMappingURL=container.js.map