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
exports.ChartComponent = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var core_1 = require("../core");
var renderer_1 = require("../app/renderer");
var specification_1 = require("../core/specification");
/** A React component that manages a sub-chart */
var ChartComponent = /** @class */ (function (_super) {
    __extends(ChartComponent, _super);
    function ChartComponent(props) {
        var _this = _super.call(this, props) || this;
        _this.recreateManager(props);
        _this.updateWithNewProps(props);
        if (props.sync) {
            _this.manager.solveConstraints();
            _this.state = {
                working: false,
                graphics: _this.renderer.render(),
            };
        }
        else {
            _this.state = {
                working: true,
                graphics: null,
            };
            _this.scheduleUpdate();
        }
        return _this;
    }
    ChartComponent.prototype.applySelection = function (selection) {
        this.manager.enumeratePlotSegments(function (cls) {
            var e_1, _a;
            try {
                for (var _b = __values(core_1.zip(cls.state.dataRowIndices, cls.state.glyphs)), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var _d = __read(_c.value, 2), rowIndices = _d[0], glyphState = _d[1];
                    if (selection == null) {
                        glyphState.emphasized = true;
                    }
                    else {
                        glyphState.emphasized = selection.isSelected(cls.object.table, rowIndices);
                    }
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_1) throw e_1.error; }
            }
        });
    };
    /**
     * TODO rework the method https://reactjs.org/blog/2018/03/27/update-on-async-rendering.html
     * @param newProps React component properties
     */
    ChartComponent.prototype.componentWillReceiveProps = function (newProps) {
        var _this = this;
        if (this.updateWithNewProps(newProps)) {
            setTimeout(function () { return _this.setState({ working: true }); });
            this.scheduleUpdate();
        }
        else if (newProps.selection != this.props.selection) {
            this.applySelection(newProps.selection);
            setTimeout(function () {
                return _this.setState({
                    graphics: _this.renderer.render(),
                });
            });
        }
        else {
            setTimeout(function () {
                var _a;
                if ((_a = newProps.renderEvents) === null || _a === void 0 ? void 0 : _a.afterRendered) {
                    newProps.renderEvents.afterRendered();
                }
            });
        }
    };
    ChartComponent.prototype.isEqual = function (a, b) {
        if (a == b) {
            return true;
        }
        return JSON.stringify(a) == JSON.stringify(b);
    };
    ChartComponent.prototype.updateWithNewProps = function (newProps) {
        var changed = false;
        if (!this.isEqual(newProps.chart, this.props.chart)) {
            this.recreateManager(newProps);
            changed = true;
        }
        else if (!this.isEqual(newProps.dataset, this.props.dataset)) {
            this.manager.setDataset(newProps.dataset);
            changed = true;
        }
        else if (!this.isEqual(newProps.defaultAttributes, this.props.defaultAttributes)) {
            this.recreateManager(newProps);
            changed = true;
        }
        if (!this.manager.chart.mappings.width ||
            newProps.width !=
                this.manager.chart.mappings.width.value) {
            this.manager.chart.mappings.width = {
                type: specification_1.MappingType.value,
                value: newProps.width,
            };
            changed = true;
        }
        if (!this.manager.chart.mappings.height ||
            newProps.height !=
                this.manager.chart.mappings.height.value) {
            this.manager.chart.mappings.height = {
                type: specification_1.MappingType.value,
                value: newProps.height,
            };
            changed = true;
        }
        return changed;
    };
    ChartComponent.prototype.recreateManager = function (props) {
        var _this = this;
        this.manager = new core_1.Prototypes.ChartStateManager(core_1.deepClone(props.chart), props.dataset, null, props.defaultAttributes);
        this.renderer = new core_1.Graphics.ChartRenderer(this.manager, props.renderEvents);
        this.manager.onUpdate(function () {
            _this.manager.solveConstraints();
            _this.setState({
                graphics: _this.renderer.render(),
            });
            _this.scheduleUpdate();
        });
    };
    ChartComponent.prototype.scheduleUpdate = function () {
        var _this = this;
        if (this.timer) {
            clearTimeout(this.timer);
        }
        this.timer = setTimeout(function () {
            _this.timer = null;
            _this.manager.solveConstraints();
            _this.applySelection(_this.props.selection);
            _this.setState({
                working: false,
                graphics: _this.renderer.render(),
            });
        }, 10);
    };
    ChartComponent.prototype.getProperty = function (objectID, property) {
        var obj = core_1.Prototypes.findObjectById(this.manager.chart, objectID);
        if (!obj) {
            return null;
        }
        return core_1.Prototypes.getProperty(obj, property);
    };
    ChartComponent.prototype.setProperty = function (objectID, property, value) {
        var obj = core_1.Prototypes.findObjectById(this.manager.chart, objectID);
        if (!obj) {
            return;
        }
        if (!this.isEqual(core_1.Prototypes.getProperty(obj, property), value)) {
            core_1.Prototypes.setProperty(obj, property, core_1.deepClone(value));
            this.setState({ working: true });
            this.scheduleUpdate();
        }
    };
    ChartComponent.prototype.getAttributeMapping = function (objectID, attribute) {
        var obj = core_1.Prototypes.findObjectById(this.manager.chart, objectID);
        if (!obj) {
            return null;
        }
        return obj.mappings[attribute];
    };
    ChartComponent.prototype.setAttributeMapping = function (objectID, attribute, mapping) {
        var obj = core_1.Prototypes.findObjectById(this.manager.chart, objectID);
        if (!obj) {
            return;
        }
        if (!this.isEqual(obj.mappings[attribute], mapping)) {
            obj.mappings[attribute] = core_1.deepClone(mapping);
            this.setState({ working: true });
            this.scheduleUpdate();
        }
    };
    ChartComponent.prototype.convertGlyphEventHandler = function (handler) {
        if (handler == null) {
            return null;
        }
        return function (element, event) {
            var _a;
            var rowIndices = element.rowIndices;
            var modifiers = {
                ctrlKey: event.ctrlKey,
                shiftKey: event.shiftKey,
                metaKey: event.metaKey,
                clientX: event.clientX,
                clientY: event.clientY,
                event: event,
            };
            handler({ table: (_a = element.plotSegment) === null || _a === void 0 ? void 0 : _a.table, rowIndices: rowIndices }, modifiers);
        };
    };
    ChartComponent.prototype.render = function () {
        var _this = this;
        var renderOptions = __assign({}, this.props.rendererOptions);
        renderOptions.onClick = this.convertGlyphEventHandler(this.props.onGlyphClick);
        renderOptions.onMouseEnter = this.convertGlyphEventHandler(this.props.onGlyphMouseEnter);
        renderOptions.onMouseLeave = this.convertGlyphEventHandler(this.props.onGlyphMouseLeave);
        renderOptions.onContextMenu = this.convertGlyphEventHandler(this.props.onGlyphContextMenuClick);
        renderOptions.selection = this.props.selection;
        var gfx = renderer_1.renderGraphicalElementSVG(this.state.graphics, renderOptions);
        var inner = (React.createElement(React.Fragment, null,
            React.createElement("defs", null, renderer_1.renderSVGDefs(this.state.graphics)),
            React.createElement("g", { transform: "translate(" + this.props.width / 2 + ", " + this.props.height / 2 + ")" },
                this.props.onGlyphClick ? (React.createElement("rect", { x: -this.props.width / 2, y: -this.props.height / 2, width: this.props.width, height: this.props.height, style: {
                        fill: "none",
                        pointerEvents: "all",
                        stroke: "none",
                    }, onClick: function () {
                        _this.props.onGlyphClick(null, null);
                    } })) : null,
                gfx,
                this.renderer.renderControls(this.manager.chart, this.manager.chartState, {
                    centerX: 0,
                    centerY: 0,
                    scale: 1,
                }),
                this.state.working ? (React.createElement("rect", { x: -this.props.width / 2, y: -this.props.height / 2, width: this.props.width, height: this.props.height, style: {
                        fill: "rgba(0, 0, 0, 0.1)",
                        stroke: "none",
                    } })) : null)));
        switch (this.props.rootElement) {
            case "svg": {
                return (React.createElement("svg", { x: 0, y: 0, width: this.props.width, height: this.props.height, className: this.props.className, style: {
                        userSelect: "none",
                    } }, inner));
            }
            case "g": {
                return React.createElement("g", { className: this.props.className }, inner);
            }
        }
    };
    return ChartComponent;
}(React.Component));
exports.ChartComponent = ChartComponent;
//# sourceMappingURL=chart_component.js.map