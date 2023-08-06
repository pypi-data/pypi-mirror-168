"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
Object.defineProperty(exports, "__esModule", { value: true });
exports.fontList = exports.primaryButtonStyles = exports.defaultDigitsGroup = exports.defaultCurrencySymbol = exports.defaultCurrency = exports.defaultNumberFormat = exports.defaultDelimiter = exports.ImageKeyColumn = exports.KeyColumn = exports.isReservedColumnName = exports.LinkTargetKeyColumn = exports.LinkSourceKeyColumn = exports.messageTypes = exports.MessageType = void 0;
var MessageType;
(function (MessageType) {
    MessageType[MessageType["GeneralError"] = 0] = "GeneralError";
    MessageType[MessageType["ParsingDataError"] = 1] = "ParsingDataError";
    MessageType[MessageType["ConstraintSolvingError"] = 2] = "ConstraintSolvingError";
    MessageType[MessageType["LinkGuideCreatingError"] = 3] = "LinkGuideCreatingError";
    MessageType[MessageType["InvalidLinksData"] = 4] = "InvalidLinksData";
    MessageType[MessageType["NoID"] = 5] = "NoID";
    MessageType[MessageType["NoSourceOrTargetID"] = 6] = "NoSourceOrTargetID";
})(MessageType = exports.MessageType || (exports.MessageType = {}));
exports.messageTypes = Object.values(MessageType);
exports.LinkSourceKeyColumn = "source_id";
exports.LinkTargetKeyColumn = "target_id";
exports.isReservedColumnName = function (name) {
    return (name === exports.LinkSourceKeyColumn ||
        name === exports.LinkTargetKeyColumn ||
        name === exports.KeyColumn ||
        name === exports.ImageKeyColumn);
};
exports.KeyColumn = "id";
exports.ImageKeyColumn = "imageId";
exports.defaultDelimiter = ",";
exports.defaultNumberFormat = Object.freeze({
    remove: ",",
    decimal: ".",
});
exports.defaultCurrency = ["$", ""];
exports.defaultCurrencySymbol = "$";
exports.defaultDigitsGroup = [3];
exports.primaryButtonStyles = {
    root: {
        backgroundColor: "#F2C811",
        color: "black",
        borderRadius: 2,
        borderColor: "#676666",
        height: 35,
    },
    rootHovered: {
        backgroundColor: "#F2C811",
        color: "black",
    },
    rootChecked: {
        backgroundColor: "#F2C811",
        color: "black",
    },
    rootPressed: {
        backgroundColor: "#F2C811",
        color: "black",
    },
};
exports.fontList = [
    "Arial Black",
    "Arial",
    "Comic Sans MS",
    "Consolas",
    "Courier New",
    "Geneva",
    "Georgia",
    "Helvetica",
    "Impact",
    "Inconsolata",
    "Lato",
    "Lucida Console",
    "Lucida Grande",
    "Palatino",
    "Segoe UI",
    "Segoe UI Light",
    "Segoe UI Semibold",
    "Segoe UI Bold",
    "Tahoma",
    "Times",
    "Trebuchet MS",
    "Verdana",
];
//# sourceMappingURL=constants.js.map