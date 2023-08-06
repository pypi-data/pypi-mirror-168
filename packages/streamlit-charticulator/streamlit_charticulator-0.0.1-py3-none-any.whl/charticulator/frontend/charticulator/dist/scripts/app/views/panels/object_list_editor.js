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
exports.ReorderListView = exports.ObjectListEditor = void 0;
var React = require("react");
var R = require("../../resources");
var core_1 = require("../../../core");
var actions_1 = require("../../actions");
var components_1 = require("../../components");
var context_component_1 = require("../../context_component");
var stores_1 = require("../../stores");
var utils_1 = require("../../utils");
var controls_1 = require("./widgets/controls");
var ObjectListEditor = /** @class */ (function (_super) {
    __extends(ObjectListEditor, _super);
    function ObjectListEditor() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ObjectListEditor.prototype.componentDidMount = function () {
        var _this = this;
        this.tokens = [];
        this.tokens.push(this.store.addListener(stores_1.AppStore.EVENT_GRAPHICS, function () { return _this.forceUpdate(); }));
        this.tokens.push(this.store.addListener(stores_1.AppStore.EVENT_SELECTION, function () { return _this.forceUpdate(); }));
    };
    ObjectListEditor.prototype.componentWillUnmount = function () {
        var e_1, _a;
        try {
            for (var _b = __values(this.tokens), _c = _b.next(); !_c.done; _c = _b.next()) {
                var token = _c.value;
                token.remove();
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
    };
    ObjectListEditor.prototype.renderChart = function () {
        var _this = this;
        var chart = this.store.chart;
        var sel = this.store.currentSelection;
        return (React.createElement("div", null,
            React.createElement("div", { tabIndex: 0, className: utils_1.classNames("el-object-item", ["is-active", sel == null]), onClick: function () {
                    _this.dispatch(new actions_1.Actions.ClearSelection());
                }, onKeyPress: function (e) {
                    if (e.key === "Enter") {
                        _this.dispatch(new actions_1.Actions.ClearSelection());
                    }
                } },
                React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(core_1.Prototypes.ObjectClasses.GetMetadata(chart.classID).iconPath) }),
                React.createElement("span", { className: "el-text" }, chart.properties.name)),
            React.createElement(ReorderListView, { enabled: true, onReorder: function (a, b) {
                    _this.dispatch(new actions_1.Actions.ReorderChartElement(a, b));
                } }, chart.elements.map(function (element) {
                return (React.createElement("div", { tabIndex: 0, className: utils_1.classNames("el-object-item", [
                        "is-active",
                        sel instanceof stores_1.ChartElementSelection &&
                            sel.chartElement == element,
                    ]), onClick: function () {
                        _this.dispatch(new actions_1.Actions.SelectChartElement(element));
                        _this.dispatch(new actions_1.Actions.SearchUpdated(""));
                    }, onKeyPress: function (e) {
                        if (e.key === "Enter") {
                            _this.dispatch(new actions_1.Actions.SelectChartElement(element));
                            _this.dispatch(new actions_1.Actions.SearchUpdated(""));
                        }
                    }, key: element._id },
                    React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(core_1.Prototypes.ObjectClasses.GetMetadata(element.classID)
                            .iconPath) }),
                    React.createElement("span", { className: "el-text" }, element.properties.name),
                    React.createElement(controls_1.Button, { icon: element.properties.visible
                            ? "general/eye"
                            : "general/eye-faded", title: "Toggle visibility", active: false, onClick: function () {
                            _this.dispatch(new actions_1.Actions.SetObjectProperty(element, "visible", null, !element.properties.visible, true));
                        } }),
                    React.createElement(controls_1.Button, { icon: "general/eraser", title: "Remove", active: false, onClick: function () {
                            _this.dispatch(new actions_1.Actions.DeleteChartElement(element));
                        } })));
            }))));
    };
    ObjectListEditor.prototype.renderGlyph = function (glyph) {
        var _this = this;
        var sel = this.store.currentSelection;
        return (React.createElement("div", { key: glyph._id },
            React.createElement("div", { tabIndex: 0, className: utils_1.classNames("el-object-item", [
                    "is-active",
                    sel instanceof stores_1.GlyphSelection && sel.glyph == glyph,
                ]), onClick: function () {
                    _this.dispatch(new actions_1.Actions.SelectGlyph(null, glyph));
                }, onKeyPress: function (e) {
                    if (e.key === "Enter") {
                        _this.dispatch(new actions_1.Actions.SelectGlyph(null, glyph));
                    }
                } },
                React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(core_1.Prototypes.ObjectClasses.GetMetadata(glyph.classID).iconPath) }),
                React.createElement("span", { className: "el-text" }, glyph.properties.name)),
            React.createElement(ReorderListView, { enabled: true, onReorder: function (a, b) {
                    _this.dispatch(new actions_1.Actions.ReorderGlyphMark(glyph, a + 1, b + 1));
                } }, glyph.marks
                .filter(function (x) { return x.classID != "mark.anchor"; })
                .map(function (mark) {
                return (React.createElement("div", { tabIndex: 0, className: utils_1.classNames("el-object-item", [
                        "is-active",
                        sel instanceof stores_1.MarkSelection &&
                            sel.glyph == glyph &&
                            sel.mark == mark,
                    ]), key: mark._id, onClick: function () {
                        _this.dispatch(new actions_1.Actions.SelectMark(null, glyph, mark));
                    }, onKeyPress: function (e) {
                        if (e.key === "Enter") {
                            _this.dispatch(new actions_1.Actions.SelectMark(null, glyph, mark));
                        }
                    } },
                    React.createElement(components_1.SVGImageIcon, { url: R.getSVGIcon(core_1.Prototypes.ObjectClasses.GetMetadata(mark.classID)
                            .iconPath) }),
                    React.createElement("span", { className: "el-text" }, mark.properties.name),
                    React.createElement(controls_1.Button, { icon: mark.properties.visible
                            ? "general/eye"
                            : "general/eye-faded", title: "Toggle visibility", active: false, onClick: function () {
                            _this.dispatch(new actions_1.Actions.SetObjectProperty(mark, "visible", null, !mark.properties.visible, true));
                        } }),
                    React.createElement(controls_1.Button, { icon: "general/eraser", active: false, title: "Remove", onClick: function () {
                            _this.dispatch(new actions_1.Actions.RemoveMarkFromGlyph(glyph, mark));
                        } })));
            }))));
    };
    ObjectListEditor.prototype.render = function () {
        var _this = this;
        var chart = this.store.chart;
        return (React.createElement("div", { className: "charticulator__object-list-editor" },
            this.renderChart(),
            chart.glyphs.map(function (glyph) { return _this.renderGlyph(glyph); })));
    };
    return ObjectListEditor;
}(context_component_1.ContextedComponent));
exports.ObjectListEditor = ObjectListEditor;
var ReorderListView = /** @class */ (function (_super) {
    __extends(ReorderListView, _super);
    function ReorderListView(props) {
        var _this = _super.call(this, props) || this;
        _this.container2Index = new WeakMap();
        _this.index2Container = new Map();
        _this.state = {
            reordering: false,
            dragIndex: null,
            dropIndex: null,
        };
        return _this;
    }
    ReorderListView.prototype.getItemAtPoint = function (x, y) {
        var e_2, _a;
        var el = document.elementFromPoint(x, y);
        while (el) {
            if (this.container2Index.has(el)) {
                var bbox = el.getBoundingClientRect();
                var ratio = (y - bbox.top) / bbox.height;
                return [this.container2Index.get(el), ratio];
            }
            el = el.parentElement;
        }
        // Couldn't find
        var minY = null, maxY = null, minIndex = null, maxIndex = null;
        try {
            for (var _b = __values(this.index2Container.entries()), _c = _b.next(); !_c.done; _c = _b.next()) {
                var _d = __read(_c.value, 2), index = _d[0], element = _d[1];
                var bbox = element.getBoundingClientRect();
                if (minY == null || minY > bbox.top) {
                    minY = bbox.top;
                    minIndex = index;
                }
                if (maxY == null || maxY < bbox.top + bbox.height) {
                    maxY = bbox.top + bbox.height;
                    maxIndex = index;
                }
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_2) throw e_2.error; }
        }
        if (y < minY) {
            return [minIndex, 0];
        }
        if (y > maxY) {
            return [maxIndex, 1];
        }
        return null;
    };
    ReorderListView.prototype.componentDidMount = function () {
        var _this = this;
        if (!this.props.enabled) {
            return;
        }
        var hammer = new Hammer(this.container);
        this.hammer = hammer;
        hammer.add(new Hammer.Pan());
        hammer.on("panstart", function (e) {
            var cx = e.center.x - e.deltaX;
            var cy = e.center.y - e.deltaY;
            var item = _this.getItemAtPoint(cx, cy);
            if (item != null) {
                _this.setState({
                    reordering: true,
                    dragIndex: item[0],
                    dropIndex: item,
                });
            }
        });
        hammer.on("pan", function (e) {
            var cx = e.center.x;
            var cy = e.center.y;
            var item = _this.getItemAtPoint(cx, cy);
            _this.setState({
                reordering: true,
                dropIndex: item,
            });
        });
        hammer.on("panend", function (e) {
            if (!_this.state.reordering || !_this.state.dropIndex) {
                return;
            }
            if (_this.props.restrict) {
                var box = e.target.getBoundingClientRect();
                var dropCoordinates = e.center;
                if (dropCoordinates.x < box.left ||
                    dropCoordinates.x > box.right ||
                    dropCoordinates.y < box.top ||
                    dropCoordinates.y > box.bottom) {
                    _this.setState({
                        reordering: false,
                        dragIndex: null,
                        dropIndex: null,
                    });
                    return;
                }
            }
            var from = _this.state.dragIndex;
            var to = _this.state.dropIndex[0] + (_this.state.dropIndex[1] > 0.5 ? 1 : 0);
            _this.setState({
                reordering: false,
                dragIndex: null,
                dropIndex: null,
            });
            _this.props.onReorder(from, to);
        });
    };
    ReorderListView.prototype.componentWillUnmount = function () {
        if (this.hammer) {
            this.hammer.destroy();
        }
    };
    ReorderListView.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", { className: "charticulator__reorder-list-view", ref: function (e) { return (_this.container = e); } }, React.Children.map(this.props.children, function (item, index) {
            return (React.createElement("div", { className: "charticulator__reorder-list-view-item", ref: function (e) {
                    if (e) {
                        _this.container2Index.set(e, index);
                        _this.index2Container.set(index, e);
                    }
                    else {
                        _this.index2Container.delete(index);
                    }
                } },
                item,
                _this.state.reordering &&
                    _this.state.dropIndex &&
                    _this.state.dropIndex[0] == index ? (React.createElement("div", { className: utils_1.classNames("charticulator__reorder-list-view-item-hint", ["is-top", _this.state.dropIndex[1] < 0.5]) })) : null,
                _this.state.reordering && _this.state.dragIndex == index ? (React.createElement("div", { className: "charticulator__reorder-list-view-item-drag-hint" })) : null));
        })));
    };
    ReorderListView.ReorderArray = function (array, dragIndex, dropIndex) {
        var x = array.splice(dragIndex, 1)[0];
        if (dragIndex < dropIndex) {
            array.splice(dropIndex - 1, 0, x);
        }
        else {
            array.splice(dropIndex, 0, x);
        }
    };
    return ReorderListView;
}(React.Component));
exports.ReorderListView = ReorderListView;
//# sourceMappingURL=object_list_editor.js.map