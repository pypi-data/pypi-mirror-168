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
Object.defineProperty(exports, "__esModule", { value: true });
exports.BingMapService = exports.GoogleMapService = exports.StaticMapService = void 0;
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var strings_1 = require("../../../../strings");
var config_1 = require("../../../config");
var StaticMapService = /** @class */ (function () {
    function StaticMapService() {
    }
    StaticMapService.prototype.getImageryAtPoint = function (options) {
        var _this = this;
        return new Promise(function (resolve, reject) {
            var url = _this.getImageryURLAtPoint(options);
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
        });
    };
    StaticMapService.GetService = function () {
        if (StaticMapService.cachedService == null) {
            var config = config_1.getConfig();
            if (config.MapService) {
                switch (config.MapService.provider) {
                    case "Google":
                        {
                            StaticMapService.cachedService = new GoogleMapService(config.MapService.apiKey);
                        }
                        break;
                    case "Bing":
                        {
                            StaticMapService.cachedService = new BingMapService(config.MapService.apiKey);
                        }
                        break;
                }
            }
        }
        return StaticMapService.cachedService;
    };
    StaticMapService.cachedService = null;
    return StaticMapService;
}());
exports.StaticMapService = StaticMapService;
function buildQueryParameters(options) {
    var r = [];
    for (var p in options) {
        if (Object.prototype.hasOwnProperty.call(options, p)) {
            r.push(encodeURIComponent(p) + "=" + encodeURIComponent(options[p]));
        }
    }
    return r.join("&");
}
var GoogleMapService = /** @class */ (function (_super) {
    __extends(GoogleMapService, _super);
    function GoogleMapService(apiKey) {
        var _this = _super.call(this) || this;
        _this.apiKey = apiKey;
        return _this;
    }
    GoogleMapService.prototype.getImageryURLAtPoint = function (options) {
        var params = {
            center: options.center.latitude + "," + options.center.longitude,
            zoom: "" + options.zoom,
            size: options.width + "x" + options.height,
            key: this.apiKey,
            format: "png",
        };
        if (options.resolution == "high") {
            params.scale = "2";
        }
        if (options.type == "satellite") {
            params.maptype = "satellite";
        }
        if (options.type == "hybrid") {
            params.maptype = "hybrid";
        }
        if (options.type == "terrain") {
            params.maptype = "terrain";
        }
        var url = "https://maps.googleapis.com/maps/api/staticmap";
        url += "?" + buildQueryParameters(params);
        return url;
    };
    return GoogleMapService;
}(StaticMapService));
exports.GoogleMapService = GoogleMapService;
var BingMapService = /** @class */ (function (_super) {
    __extends(BingMapService, _super);
    function BingMapService(apiKey) {
        var _this = _super.call(this) || this;
        _this.apiKey = apiKey;
        return _this;
    }
    BingMapService.prototype.getImageryURLAtPoint = function (options) {
        var params = {
            mapSize: options.width + "," + options.height,
            key: this.apiKey,
            format: "png",
        };
        if (options.resolution == "high") {
            params.dpi = "Large";
            params.mapSize = options.width * 2 + "," + options.height * 2;
        }
        var type = "Road";
        if (options.type == "satellite") {
            type = "Aerial";
        }
        if (options.type == "hybrid") {
            type = "AerialWithLabels";
        }
        var url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/" + type + "/";
        url += options.center.latitude + "," + options.center.longitude + "/" + (options.zoom + 1);
        url += "?" + buildQueryParameters(params);
        return url;
    };
    return BingMapService;
}(StaticMapService));
exports.BingMapService = BingMapService;
//# sourceMappingURL=map_service.js.map