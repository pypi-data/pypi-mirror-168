"use strict";
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
exports.CollapsiblePanel = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var react_1 = require("@fluentui/react");
var React = require("react");
var react_2 = require("react");
var fluentui_customized_components_1 = require("./fluentui_customized_components");
var app_1 = require("../../../../../app");
var types_1 = require("../../../../../core/specification/types");
var core_1 = require("../../../../../core");
var contextMenuCallout_1 = require("./contextMenuCallout");
// eslint-disable-next-line max-lines-per-function
exports.CollapsiblePanel = function (_a) {
    var header = _a.header, widgets = _a.widgets, isCollapsed = _a.isCollapsed, alignVertically = _a.alignVertically, store = _a.store;
    var collapsePanel = store
        ? false
        : isCollapsed === undefined
            ? false
            : isCollapsed;
    var _b = __read(React.useState(collapsePanel), 2), groupState = _b[0], setGroupState = _b[1];
    var _c = __read(React.useState(false), 2), calloutVisible = _c[0], setCalloutVisible = _c[1];
    react_2.useEffect(function () {
        var collapsePanel = store
            ? (store === null || store === void 0 ? void 0 : store.collapseOrExpandPanelsType) === types_1.CollapseOrExpandPanels.Collapse
            : isCollapsed === undefined
                ? false
                : isCollapsed;
        setGroupState(collapsePanel);
    }, [store, store === null || store === void 0 ? void 0 : store.collapseOrExpandPanelsType, isCollapsed]);
    var calloutId = "calloutId-" + core_1.getRandomNumber();
    var onContextMenu = React.useCallback(function (event) {
        event.preventDefault();
        setCalloutVisible(!calloutVisible);
    }, [calloutVisible]);
    return (React.createElement(fluentui_customized_components_1.FluentGroupedList, { marginLeft: alignVertically ? 0 : null },
        React.createElement(react_1.GroupedList, { groupProps: {
                onRenderHeader: function (props) {
                    return (React.createElement(react_1.GroupHeader, __assign({ onRenderGroupHeaderCheckbox: function () { return null; } }, props, { styles: fluentui_customized_components_1.groupHeaderStyles, onToggleCollapse: function (group) {
                            setGroupState(!group.isCollapsed);
                            if (store) {
                                store.dispatcher.dispatch(new app_1.Actions.ExpandOrCollapsePanelsUpdated(types_1.CollapseOrExpandPanels.Custom));
                            }
                        }, onGroupHeaderClick: function (group) {
                            props.onToggleCollapse(group);
                            setGroupState(group.isCollapsed);
                        }, onRenderTitle: typeof header === "string"
                            ? function () { return (React.createElement(react_1.Label, { onContextMenu: onContextMenu, id: calloutId, style: {
                                    width: "100%",
                                } }, header)); }
                            : header })));
                },
            }, selectionMode: react_1.SelectionMode.none, items: widgets
                .filter(function (w) { return (Array.isArray(w) ? (w === null || w === void 0 ? void 0 : w[0]) != null : w != null); })
                .map(function (w, i) { return ({
                key: i,
                item: w,
            }); }), onRenderCell: function (nestingDepth, item, itemIndex) {
                return item &&
                    item.item &&
                    typeof itemIndex === "number" &&
                    itemIndex > -1 ? (React.createElement("div", { className: "charticulator__widget-collapsible-panel-item", key: itemIndex }, item.item)) : null;
            }, groups: [
                {
                    count: widgets.length,
                    key: "group",
                    level: 0,
                    name: typeof header === "string" ? header : "",
                    startIndex: 0,
                    isCollapsed: groupState,
                },
            ], compact: true, styles: __assign(__assign({}, fluentui_customized_components_1.groupStyles), { groupIsDropping: {} }), focusZoneProps: {
                handleTabKey: 1,
            } }),
        React.createElement(contextMenuCallout_1.ContextMenuCallout, { store: store, calloutId: calloutId, hideCallout: function (value) { return setCalloutVisible(value); }, calloutVisible: calloutVisible })));
};
//# sourceMappingURL=collapsiblePanel.js.map