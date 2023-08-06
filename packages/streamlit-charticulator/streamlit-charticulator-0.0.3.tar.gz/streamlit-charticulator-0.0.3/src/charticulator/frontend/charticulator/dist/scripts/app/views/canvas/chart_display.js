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
Object.defineProperty(exports, "__esModule", { value: true });
exports.renderChartToLocalString = exports.renderChartToString = exports.ChartDisplayView = void 0;
var React = require("react");
var ReactDOMServer = require("react-dom/server");
var core_1 = require("../../../core");
var strings_1 = require("../../../strings");
var renderer_1 = require("../../renderer");
var ChartDisplayView = /** @class */ (function (_super) {
    __extends(ChartDisplayView, _super);
    function ChartDisplayView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ChartDisplayView.prototype.render = function () {
        var chartState = this.props.manager.chartState;
        var width = chartState.attributes.width;
        var height = chartState.attributes.height;
        var renderer = new core_1.Graphics.ChartRenderer(this.props.manager);
        var graphics = renderer.render();
        return (React.createElement("svg", { x: 0, y: 0, width: width, height: height, viewBox: "0 0 " + width.toFixed(6) + " " + height.toFixed(6), 
            /* eslint-disable-next-line */
            xmlns: "http://www.w3.org/2000/svg", 
            /* eslint-disable-next-line */
            xmlnsXlink: "http://www.w3.org/1999/xlink", xmlSpace: "preserve" },
            React.createElement("g", { transform: "translate(" + (width / 2).toFixed(6) + "," + (height / 2).toFixed(6) + ")" },
                React.createElement(renderer_1.GraphicalElementDisplay, { element: graphics }),
                renderer.renderControls(this.props.manager.chart, this.props.manager.chartState, {
                    centerX: 0,
                    centerY: 0,
                    scale: 1,
                }))));
    };
    return ChartDisplayView;
}(React.Component));
exports.ChartDisplayView = ChartDisplayView;
function renderChartToString(dataset, chart, chartState) {
    var manager = new core_1.Prototypes.ChartStateManager(chart, dataset, chartState);
    return ReactDOMServer.renderToString(React.createElement(ChartDisplayView, { manager: manager }));
}
exports.renderChartToString = renderChartToString;
function renderChartToLocalString(dataset, chart, chartState) {
    var manager = new core_1.Prototypes.ChartStateManager(chart, dataset, chartState);
    var width = chartState.attributes.width;
    var height = chartState.attributes.height;
    var renderer = new core_1.Graphics.ChartRenderer(manager);
    var graphics = renderer.render();
    var urls = new Map();
    var allTasks = [];
    renderer_1.renderGraphicalElementSVG(graphics, {
        chartComponentSync: true,
        externalResourceResolver: function (url) {
            var task = new Promise(function (resolve, reject) {
                var img = new Image();
                img.setAttribute("crossOrigin", "anonymous");
                img.onload = function () {
                    var canvas = document.createElement("canvas");
                    canvas.width = img.width;
                    canvas.height = img.height;
                    canvas.getContext("2d").drawImage(img, 0, 0);
                    resolve(canvas.toDataURL("image/png"));
                };
                img.onerror = function () {
                    reject(new Error(strings_1.strings.error.imageLoad(url)));
                };
                img.src = url;
            }).then(function (dataurl) {
                urls.set(url, dataurl);
            });
            allTasks.push(task);
            return url;
        },
    });
    return Promise.all(allTasks).then(function () {
        return ReactDOMServer.renderToString(React.createElement("svg", { x: 0, y: 0, width: width, height: height, viewBox: "0 0 " + width.toFixed(6) + " " + height.toFixed(6), 
            /* eslint-disable-next-line */
            xmlns: "http://www.w3.org/2000/svg", 
            /* eslint-disable-next-line */
            xmlnsXlink: "http://www.w3.org/1999/xlink", xmlSpace: "preserve" },
            React.createElement("defs", null, renderer_1.renderSVGDefs(graphics)),
            React.createElement("g", { transform: "translate(" + (width / 2).toFixed(6) + "," + (height / 2).toFixed(6) + ")" }, renderer_1.renderGraphicalElementSVG(graphics, {
                chartComponentSync: true,
                externalResourceResolver: function (url) { return urls.get(url); },
            }))));
    });
}
exports.renderChartToLocalString = renderChartToLocalString;
//# sourceMappingURL=chart_display.js.map