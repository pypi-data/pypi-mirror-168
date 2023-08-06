"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
/* eslint-disable @typescript-eslint/no-namespace */
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
var __spread = (this && this.__spread) || function () {
    for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
    return ar;
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.Scale = void 0;
var d3_scale_1 = require("d3-scale");
var d3_time_format_1 = require("d3-time-format");
var _1 = require(".");
var types_1 = require("../specification/types");
var Scale;
(function (Scale) {
    /** Base scale class */
    var BaseScale = /** @class */ (function () {
        function BaseScale() {
        }
        /** Get mapped values */
        BaseScale.prototype.map = function (values) {
            var _this = this;
            return values.map(function (x) { return (x == null ? null : _this.get(x)); });
        };
        return BaseScale;
    }());
    Scale.BaseScale = BaseScale;
    var LinearScale = /** @class */ (function (_super) {
        __extends(LinearScale, _super);
        function LinearScale() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        LinearScale.prototype.inferParameters = function (values) {
            values = values.filter(function (v) { return !isNaN(v); });
            var scale = d3_scale_1.scaleLinear()
                .domain([Math.min.apply(Math, __spread(values)), Math.max.apply(Math, __spread(values))])
                .nice();
            this.domainMin = scale.domain()[0];
            this.domainMax = scale.domain()[1];
            if (this.domainMax == this.domainMin) {
                this.domainMax = this.domainMin + 1;
            }
        };
        LinearScale.prototype.adjustDomain = function (options) {
            if (options.startWithZero == "default" || options.startWithZero == null) {
                if (this.domainMin > 0) {
                    this.domainMin = 0;
                }
            }
            else if (options.startWithZero == "always") {
                this.domainMin = 0;
            }
        };
        LinearScale.prototype.get = function (v) {
            return (v - this.domainMin) / (this.domainMax - this.domainMin);
        };
        LinearScale.prototype.ticks = function (n) {
            if (n === void 0) { n = 10; }
            var scale = d3_scale_1.scaleLinear().domain([this.domainMin, this.domainMax]);
            return scale.ticks(n);
        };
        LinearScale.prototype.tickFormat = function (n, specifier) {
            if (n === void 0) { n = 10; }
            var scale = d3_scale_1.scaleLinear().domain([this.domainMin, this.domainMax]);
            return scale.tickFormat(n, specifier);
        };
        return LinearScale;
    }(BaseScale));
    Scale.LinearScale = LinearScale;
    var LogarithmicScale = /** @class */ (function (_super) {
        __extends(LogarithmicScale, _super);
        function LogarithmicScale() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        LogarithmicScale.prototype.inferParameters = function (values) {
            var min = Math.min.apply(Math, __spread(values));
            var scale = d3_scale_1.scaleLog()
                .domain([min <= 0 ? 1 : min, Math.max.apply(Math, __spread(values))])
                .nice();
            this.domainMin = scale.domain()[0];
            this.domainMax = scale.domain()[1];
            if (this.domainMax == this.domainMin) {
                this.domainMax = this.domainMin + 1;
            }
        };
        LogarithmicScale.prototype.get = function (v) {
            return ((Math.log(v) - Math.log(this.domainMin)) /
                (Math.log(this.domainMax) - Math.log(this.domainMin)));
        };
        LogarithmicScale.prototype.ticks = function (n) {
            if (n === void 0) { n = 10; }
            var scale = d3_scale_1.scaleLog().domain([this.domainMin, this.domainMax]);
            return scale.ticks(n);
        };
        LogarithmicScale.prototype.tickFormat = function (n, specifier) {
            if (n === void 0) { n = 10; }
            var scale = d3_scale_1.scaleLog().domain([this.domainMin, this.domainMax]);
            return scale.tickFormat(n, specifier);
        };
        return LogarithmicScale;
    }(BaseScale));
    Scale.LogarithmicScale = LogarithmicScale;
    var DateScale = /** @class */ (function (_super) {
        __extends(DateScale, _super);
        function DateScale() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        DateScale.prototype.inferParameters = function (values, nice) {
            if (nice === void 0) { nice = true; }
            var filteredValues = values.filter(function (val) { return !isNaN(val); });
            var scale = (_1.isUtcTimeZone() ? d3_scale_1.scaleUtc() : d3_scale_1.scaleTime()).domain([
                Math.min.apply(Math, __spread(filteredValues)),
                Math.max.apply(Math, __spread(filteredValues)),
            ]);
            if (nice) {
                scale = scale.nice();
            }
            this.domainMin = scale.domain()[0].getTime();
            this.domainMax = scale.domain()[1].getTime();
            if (this.domainMax == this.domainMin) {
                this.domainMax = this.domainMin + 1000; // 1 second difference
            }
        };
        DateScale.prototype.ticks = function (n) {
            if (n === void 0) { n = 10; }
            var scale = (_1.isUtcTimeZone() ? d3_scale_1.scaleUtc() : d3_scale_1.scaleTime()).domain([this.domainMin, this.domainMax]);
            return scale.ticks(n).map(function (x) { return x.getTime(); });
        };
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        DateScale.prototype.tickFormat = function (_n, specifier) {
            if (_n === void 0) { _n = 10; }
            var fmt = _1.isUtcTimeZone() ? d3_time_format_1.utcFormat(specifier) : d3_time_format_1.timeFormat(specifier);
            return function (t) { return fmt(new Date(t)); };
        };
        return DateScale;
    }(LinearScale));
    Scale.DateScale = DateScale;
    var CategoricalScale = /** @class */ (function (_super) {
        __extends(CategoricalScale, _super);
        function CategoricalScale() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        CategoricalScale.prototype.inferParameters = function (values, order) {
            var e_1, _a;
            if (order === void 0) { order = types_1.OrderMode.alphabetically; }
            var vals = new Map();
            var domain = [];
            try {
                for (var values_1 = __values(values), values_1_1 = values_1.next(); !values_1_1.done; values_1_1 = values_1.next()) {
                    var v = values_1_1.value;
                    if (v == null) {
                        continue;
                    }
                    v = v.toString();
                    if (vals.has(v)) {
                        vals.set(v, vals.get(v) + 1);
                    }
                    else {
                        vals.set(v, 1);
                        domain.push(v);
                    }
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (values_1_1 && !values_1_1.done && (_a = values_1.return)) _a.call(values_1);
                }
                finally { if (e_1) throw e_1.error; }
            }
            // Sort alphabetically
            switch (order) {
                case "alphabetically":
                    {
                        domain.sort(_1.getSortFunctionByData(domain));
                    }
                    break;
                case "occurrence":
                    {
                        domain.sort(function (a, b) {
                            var ca = vals.get(a);
                            var cb = vals.get(b);
                            if (ca != cb) {
                                return cb - ca;
                            }
                            else {
                                return a < b ? -1 : 1;
                            }
                        });
                    }
                    break;
                // case "order":
                //   {
                //   }
                //   break;
            }
            this.domain = new Map();
            for (var i = 0; i < domain.length; i++) {
                this.domain.set(domain[i], i);
            }
            this.length = domain.length;
        };
        CategoricalScale.prototype.get = function (v) {
            return this.domain.get(v);
        };
        return CategoricalScale;
    }(BaseScale));
    Scale.CategoricalScale = CategoricalScale;
})(Scale = exports.Scale || (exports.Scale = {}));
//# sourceMappingURL=scales.js.map