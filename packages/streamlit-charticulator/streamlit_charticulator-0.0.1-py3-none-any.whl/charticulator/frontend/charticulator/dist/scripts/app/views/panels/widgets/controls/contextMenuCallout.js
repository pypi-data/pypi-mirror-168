"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ContextMenuCallout = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var strings_1 = require("../../../../../strings");
var app_1 = require("../../../../../app");
var types_1 = require("../../../../../core/specification/types");
var react_1 = require("@fluentui/react");
var fluentui_customized_components_1 = require("./fluentui_customized_components");
// eslint-disable-next-line max-lines-per-function
exports.ContextMenuCallout = function (_a) {
    var store = _a.store, calloutId = _a.calloutId, hideCallout = _a.hideCallout, calloutVisible = _a.calloutVisible;
    var menuItems = React.useMemo(function () {
        var items = [];
        if (store) {
            items = [
                {
                    name: strings_1.strings.panels.collapseAllCategories,
                    onClick: function () {
                        store.dispatcher.dispatch(new app_1.Actions.ExpandOrCollapsePanelsUpdated(types_1.CollapseOrExpandPanels.Collapse));
                    },
                },
                {
                    name: strings_1.strings.panels.expandAllCategories,
                    onClick: function () {
                        store.dispatcher.dispatch(new app_1.Actions.ExpandOrCollapsePanelsUpdated(types_1.CollapseOrExpandPanels.Expand));
                    },
                },
            ];
        }
        return items;
    }, [store]);
    return (React.createElement(React.Fragment, null, calloutVisible && (React.createElement(react_1.Callout, { target: "#" + calloutId, isBeakVisible: false, onRestoreFocus: function () { return hideCallout(false); }, directionalHint: 5, onDismiss: function () { return hideCallout(false); } },
        React.createElement("div", null,
            React.createElement(react_1.List, { items: menuItems, onRenderCell: function (item) {
                    var theme = react_1.getTheme();
                    return (React.createElement(fluentui_customized_components_1.FluentDataBindingMenuItem, { backgroundColorHover: theme.semanticColors.buttonBackgroundHovered, onClick: function () {
                            item.onClick();
                            hideCallout(false);
                        } },
                        React.createElement(fluentui_customized_components_1.FluentDataBindingMenuLabel, { style: {
                                padding: 5,
                            } }, item.name)));
                } }))))));
};
//# sourceMappingURL=contextMenuCallout.js.map