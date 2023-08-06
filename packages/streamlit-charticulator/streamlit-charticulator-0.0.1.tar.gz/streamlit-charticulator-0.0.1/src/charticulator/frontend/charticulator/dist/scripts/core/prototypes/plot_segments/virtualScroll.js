"use strict";
/* eslint-disable max-lines-per-function */
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
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
exports.VirtualScrollBar = void 0;
var React = require("react");
var react_1 = require("react");
var types_1 = require("../../specification/types");
exports.VirtualScrollBar = function (_a) {
    var handlerBarWidth = _a.handlerBarWidth, // AxisRenderer.SCROLL_BAR_SIZE
    vertical = _a.vertical, height = _a.height, initialPosition = _a.initialPosition, onScroll = _a.onScroll, width = _a.width, x = _a.x, y = _a.y, zoom = _a.zoom, scrollBarRatio = _a.scrollBarRatio, windowSize = _a.windowSize, dataType = _a.dataType;
    var trackSize = width;
    if (vertical) {
        trackSize = height;
    }
    var handleSize;
    if (dataType == types_1.AxisDataBindingType.Categorical) {
        handleSize = vertical ? height * scrollBarRatio : width * scrollBarRatio;
    }
    else {
        handleSize = vertical ? height / 10 : width / 10;
    }
    var mapPositionToCoordinates = React.useCallback(function (handlePosition) {
        var handlePositionX = 0;
        var handlePositionY = 0;
        if (handlePosition > 100) {
            handlePosition = 100;
        }
        if (handlePosition < 0) {
            handlePosition = 0;
        }
        handlePosition =
            ((trackSize - handlerBarWidth * 2 - handleSize) / 100) *
                (100 - handlePosition) +
                handlerBarWidth; // map % to axis position
        if (vertical) {
            handlePositionY = handlePosition;
        }
        else {
            handlePositionX = handlePosition;
        }
        return [handlePositionX, handlePositionY];
    }, [handleSize, handlerBarWidth, trackSize, vertical]);
    var _b = __read(React.useState(initialPosition), 2), position = _b[0], setPosition = _b[1];
    var _c = __read(React.useState(false), 2), isActive = _c[0], setActive = _c[1];
    react_1.useEffect(function () {
        onScroll(position);
        // eslint-disable-next-line
    }, [windowSize]);
    var _d = __read(React.useMemo(function () { return mapPositionToCoordinates(position); }, [position, mapPositionToCoordinates]), 2), handlePositionX = _d[0], handlePositionY = _d[1];
    var handlerWidth = 0;
    var handlerHeight = 0;
    var buttonsWidth = handlerBarWidth;
    var buttonsHeight = handlerBarWidth;
    if (vertical) {
        handlerHeight = handleSize;
        handlerWidth = handlerBarWidth;
    }
    else {
        handlerWidth = handleSize;
        handlerHeight = handlerBarWidth;
    }
    var track = React.useRef(null);
    var handler = React.useRef(null);
    var onMouseMove = React.useCallback(function (e) {
        if (!isActive) {
            return;
        }
        var widthPerBar = !vertical ? width / windowSize : height / windowSize;
        var widthPerBarPercent = !vertical
            ? widthPerBar / width
            : widthPerBar / height;
        var trackElement = track.current.getBoundingClientRect();
        var deltaX = e.clientX - trackElement.left;
        var deltaY = e.clientY - trackElement.top;
        var handlerElement = handler.current.getBoundingClientRect();
        var deltaXHandler = e.clientX - handlerElement.left;
        var deltaYHandler = e.clientY - handlerElement.top;
        if (deltaXHandler > 0 && deltaXHandler < handleSize * zoom.scale) {
            deltaX = deltaX - deltaXHandler;
        }
        if (deltaYHandler > 0 && deltaYHandler < handleSize * zoom.scale) {
            deltaY = deltaY - deltaYHandler;
        }
        // debugger
        var newPosition = position;
        if (vertical) {
            var trackSize_1 = Math.abs(trackElement.bottom - trackElement.top);
            newPosition = (deltaY / trackSize_1) * 100;
        }
        else {
            var trackSize_2 = Math.abs(trackElement.right - trackElement.left);
            newPosition = 100 - (deltaX / trackSize_2) * 100;
        }
        if (newPosition > 100) {
            newPosition = 100;
        }
        if (dataType == types_1.AxisDataBindingType.Categorical) {
            if (newPosition - widthPerBarPercent * 100 < 0) {
                newPosition = 0;
            }
        }
        setPosition(Math.round(newPosition));
        onScroll(Math.round(newPosition));
    }, [
        dataType,
        handleSize,
        height,
        isActive,
        onScroll,
        position,
        vertical,
        width,
        windowSize,
        zoom.scale,
        track,
        handler,
    ]);
    var onClick = React.useCallback(function (sign) {
        var newPosition = position + sign * 5;
        if (newPosition > 100) {
            newPosition = 100;
        }
        if (newPosition < 0) {
            newPosition = 0;
        }
        setPosition(Math.round(newPosition));
        onScroll(newPosition);
    }, [onScroll, position]);
    return (React.createElement(React.Fragment, null,
        React.createElement("g", { className: "controls" },
            React.createElement("rect", { ref: track, className: "track", x: Math.min(x, x + width) + (vertical ? 0 : buttonsWidth), y: -Math.max(y, y + height) + (vertical ? buttonsHeight : 0), width: Math.abs(width) - (vertical ? 0 : buttonsWidth * 2), height: Math.abs(height) - (vertical ? buttonsHeight * 2 : 0), onMouseUp: function () {
                    setActive(false);
                }, style: {
                    fill: "#e1e1e1",
                    opacity: 1,
                }, onMouseMove: onMouseMove }),
            React.createElement("rect", { ref: handler, className: "handler", x: Math.min(x + handlePositionX, x + handlePositionX + handlerWidth), y: -Math.max(y + handlePositionY, y + handlePositionY + handlerHeight), width: Math.abs(handlerWidth), height: Math.abs(handlerHeight), style: {
                    fill: "#b3b0ad",
                    opacity: 1,
                }, onMouseDown: function () {
                    setActive(true);
                }, onMouseUp: function () {
                    setActive(false);
                } }),
            vertical ? (React.createElement(React.Fragment, null,
                React.createElement("g", null,
                    React.createElement("rect", { ref: handler, className: "downButton", x: Math.min(x, x + buttonsWidth), y: -Math.max(y, y + buttonsHeight), width: Math.abs(buttonsWidth), height: Math.abs(buttonsHeight), style: {
                            fill: "#b3b0ad",
                        }, onClick: function () {
                            onClick(1);
                        } }),
                    React.createElement("path", { transform: "translate(" + (Math.min(x, x + buttonsWidth) + buttonsWidth) + ", " + (-Math.max(y, y + buttonsHeight) + buttonsWidth) + ") scale(0.005) rotate(180)", d: "M1955 1533l-931-930-931 930-90-90L1024 421l1021 1022-90 90z" })),
                React.createElement("g", null,
                    React.createElement("rect", { ref: handler, className: "upButton", x: Math.min(x, x + width), y: -Math.max(y, y + height), width: Math.abs(buttonsWidth), height: Math.abs(buttonsHeight), style: {
                            fill: "#b3b0ad",
                        }, onClick: function () {
                            onClick(-1);
                        } }),
                    React.createElement("path", { onClick: function () {
                            onClick(-1);
                        }, transform: "translate(" + Math.min(x, x + width) + ", " + -Math.max(y, y + height) + ") scale(0.005)", d: "M1955 1533l-931-930-931 930-90-90L1024 421l1021 1022-90 90z" })),
                React.createElement("rect", { className: "interaction-handler", x: Math.min(x, x + width) - height, y: -Math.max(y, y + height) - height, width: Math.abs(width) + width * 2, height: Math.abs(height) + width * 2, onMouseMove: onMouseMove, onMouseOut: function () {
                        setActive(false);
                    } }))) : (React.createElement(React.Fragment, null,
                React.createElement("g", null,
                    React.createElement("rect", { ref: handler, className: "leftButton", x: Math.min(x, x + width), y: -Math.max(y, y + height), width: Math.abs(buttonsWidth), height: Math.abs(height), style: {
                            fill: "#b3b0ad",
                        }, onClick: function () {
                            onClick(1);
                        } }),
                    React.createElement("path", { onClick: function () {
                            onClick(1);
                        }, transform: "translate(" + Math.min(x, x + width) + ", " + (-Math.max(y, y + height) + buttonsWidth) + ") scale(0.005) rotate(-90)", d: "M1955 1533l-931-930-931 930-90-90L1024 421l1021 1022-90 90z" })),
                React.createElement("g", null,
                    React.createElement("rect", { ref: handler, className: "rightButton", x: Math.max(x, x + width) - buttonsWidth, y: -Math.max(y, y + height), width: Math.abs(buttonsWidth), height: Math.abs(height), style: {
                            fill: "#b3b0ad",
                        }, onClick: function () {
                            onClick(-1);
                        } }),
                    React.createElement("path", { transform: "translate(" + Math.max(x, x + width) + ", " + -Math.max(y, y + height) + ") scale(0.005) rotate(90)", d: "M1955 1533l-931-930-931 930-90-90L1024 421l1021 1022-90 90z" })),
                React.createElement("rect", { className: "interaction-handler", x: Math.min(x, x + width) - width, y: -Math.max(y, y + height) - width, width: Math.abs(width) + height * 2, height: Math.abs(height) + height * 2, onMouseMove: onMouseMove, onMouseOut: function () {
                        setActive(false);
                    } }))))));
};
//# sourceMappingURL=virtualScroll.js.map