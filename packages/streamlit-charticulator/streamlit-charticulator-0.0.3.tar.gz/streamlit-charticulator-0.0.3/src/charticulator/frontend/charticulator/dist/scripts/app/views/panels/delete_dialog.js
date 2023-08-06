"use strict";
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
exports.DeleteDialog = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var React = require("react");
var react_1 = require("react");
var react_2 = require("@fluentui/react");
var R = require("../../resources");
var strings_1 = require("../../../strings");
var utils_1 = require("../../utils");
var actions_1 = require("../../actions");
var components_1 = require("../../components");
var core_1 = require("../../../core");
var dialogContentProps = {
    type: react_2.DialogType.normal,
    title: strings_1.strings.dialog.deleteChart,
    subText: strings_1.strings.dialog.resetConfirm,
};
exports.DeleteDialog = function (_a) {
    var context = _a.context;
    var _b = __read(react_1.useState(true), 2), isHidden = _b[0], setIsHidden = _b[1];
    var onClick = react_1.useCallback(function () {
        if (utils_1.isInIFrame()) {
            setIsHidden(false);
        }
        else {
            if (confirm(strings_1.strings.dialog.resetConfirm)) {
                new actions_1.Actions.Reset().dispatch(context.store.dispatcher);
            }
        }
    }, [context]);
    var toggleHideDialog = react_1.useCallback(function () {
        setIsHidden(true);
    }, []);
    var onDeleteChart = react_1.useCallback(function () {
        context.store.dispatcher.dispatch(new actions_1.Actions.Reset());
        setIsHidden(true);
        core_1.getDefaultColorGeneratorResetFunction()();
    }, [context]);
    return (React.createElement(React.Fragment, null,
        React.createElement(components_1.MenuButton, { url: R.getSVGIcon("toolbar/trash"), title: strings_1.strings.menuBar.reset, text: strings_1.strings.menuBar.reset, onClick: onClick }),
        React.createElement(react_2.Dialog, { hidden: isHidden, onDismiss: toggleHideDialog, dialogContentProps: dialogContentProps },
            React.createElement(react_2.DialogFooter, null,
                React.createElement(react_2.DefaultButton, { styles: core_1.primaryButtonStyles, onClick: onDeleteChart, text: strings_1.strings.button.yes }),
                React.createElement(react_2.DefaultButton, { onClick: toggleHideDialog, text: strings_1.strings.button.no })))));
};
//# sourceMappingURL=delete_dialog.js.map