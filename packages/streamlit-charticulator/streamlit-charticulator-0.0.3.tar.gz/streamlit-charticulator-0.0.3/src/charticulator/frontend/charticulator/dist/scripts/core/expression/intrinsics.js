"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.precedences = exports.operators = exports.functions = exports.constants = void 0;
var datetime_1 = require("../dataset/datetime");
var common_1 = require("../common");
var d3_time_format_1 = require("d3-time-format");
exports.constants = {};
exports.functions = {};
// eslint-disable-next-line
exports.operators = {};
exports.precedences = {
    LAMBDA_EXPRESSION: 1,
    FUNCTION_ARGUMENT: 0,
    OPERATORS: {
        "unary:not": [11, 11],
        and: [12, 12, 12],
        or: [13, 13, 13],
        ">": [14, 14, 15],
        "<": [14, 14, 15],
        ">=": [14, 14, 15],
        "<=": [14, 14, 15],
        "==": [14, 14, 15],
        "!=": [14, 14, 15],
        "+": [16, 16, 16],
        "-": [16, 16, 17],
        "*": [18, 18, 18],
        "/": [18, 18, 19],
        "^": [20, 20, 21],
        "unary:+": [22, 22],
        "unary:-": [23, 23],
    },
    FUNCTION_CALL: 100,
    LAMBDA_FUNCTION: 100,
    VARIABLE: 100,
    FIELD_ACCESS: 100,
    VALUE: 100,
};
// Math constants
exports.constants.PI = Math.PI;
exports.constants.E = Math.E;
/** Make a unary function capable of taking element-wise array input */
function makeArrayCapable1(f) {
    return function (a) {
        if (a instanceof Array) {
            return a.map(f);
        }
        else {
            return f(a);
        }
    };
}
/** Make a binary function capable of taking element-wise array input */
function makeArrayCapable2(f) {
    return function (a, b) {
        if (a instanceof Array && b instanceof Array) {
            return a.map(function (ai, i) { return f(ai, b[i]); });
        }
        else if (a instanceof Array) {
            return a.map(function (ai) { return f(ai, b); });
        }
        else if (b instanceof Array) {
            return b.map(function (bi) { return f(a, bi); });
        }
        else {
            return f(a, b);
        }
    };
}
// Math functions
exports.functions.abs = makeArrayCapable1(Math.abs);
exports.functions.sign = makeArrayCapable1(Math.sign);
exports.functions.floor = makeArrayCapable1(Math.floor);
exports.functions.ceil = makeArrayCapable1(Math.ceil);
exports.functions.exp = makeArrayCapable1(Math.exp);
exports.functions.log = makeArrayCapable1(Math.log);
exports.functions.log10 = makeArrayCapable1(Math.log10);
exports.functions.sin = makeArrayCapable1(Math.sin);
exports.functions.cos = makeArrayCapable1(Math.cos);
exports.functions.tan = makeArrayCapable1(Math.tan);
exports.functions.asin = makeArrayCapable1(Math.asin);
exports.functions.acos = makeArrayCapable1(Math.acos);
exports.functions.atan = makeArrayCapable1(Math.atan);
exports.functions.atan2 = makeArrayCapable2(Math.atan2);
exports.functions.tanh = makeArrayCapable1(Math.tanh);
exports.functions.sqrt = makeArrayCapable1(Math.sqrt);
exports.functions.pow = makeArrayCapable2(Math.pow);
// List and range
exports.functions.array = function () {
    var args = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        args[_i] = arguments[_i];
    }
    return args;
};
exports.functions.list = exports.functions.array;
exports.functions.length = function (arg) { return arg.length; };
exports.functions.range = function (min, max, step) {
    if (step === void 0) { step = 1; }
    var opt = [];
    for (var i = min; i <= max; i += step) {
        opt.push(i);
    }
    return opt;
};
// Object and fields
exports.functions.get = function (obj, field) { return obj[field]; };
// Array functions
exports.functions.first = function (list) { return list[0]; };
exports.functions.last = function (list) { return list[list.length - 1]; };
exports.functions.map = function (list, func) {
    return list.map(function (item) { return func(item); });
};
exports.functions.filter = function (list, func) {
    return list.filter(function (item) { return func(item); });
};
// Statistics
function stat_foreach(f, list) {
    for (var i = 0; i < list.length; i++) {
        var l = list[i];
        if (l instanceof Array) {
            for (var j = 0; j < l.length; j++) {
                if (l[j] != null) {
                    f(l[j]);
                }
            }
        }
        else {
            if (l != null) {
                f(l);
            }
        }
    }
}
function quantile(q, list) {
    var values = [];
    stat_foreach(function (x) {
        values.push(x);
    }, list);
    values.sort(function (a, b) { return a - b; });
    var pos = (values.length - 1) * q, base = Math.floor(pos), rest = pos - base;
    return ((values[base + 1] &&
        values[base] + rest * (values[base + 1] - values[base])) ||
        values[base]);
}
exports.functions.min = function () {
    var list = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        list[_i] = arguments[_i];
    }
    var r = null;
    stat_foreach(function (x) {
        if (r == null || x < r) {
            r = x;
        }
    }, list);
    return r;
};
exports.functions.max = function () {
    var list = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        list[_i] = arguments[_i];
    }
    var r = null;
    stat_foreach(function (x) {
        if (r == null || x > r) {
            r = x;
        }
    }, list);
    return r;
};
exports.functions.sum = function () {
    var list = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        list[_i] = arguments[_i];
    }
    var r = 0;
    stat_foreach(function (x) { return (r += x); }, list);
    return r;
};
exports.functions.count = function () {
    var list = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        list[_i] = arguments[_i];
    }
    var r = 0;
    // eslint-disable-next-line
    stat_foreach(function (x) { return (r += 1); }, list);
    return r;
};
exports.functions.stdev = function () {
    var list = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        list[_i] = arguments[_i];
    }
    var count = 0;
    var sumX = 0;
    var sumX2 = 0;
    stat_foreach(function (x) {
        count += 1;
        sumX += x;
        sumX2 += x * x;
    }, list);
    sumX2 /= count;
    sumX /= count;
    return Math.sqrt(sumX2 - sumX * sumX);
};
exports.functions.variance = function () {
    var list = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        list[_i] = arguments[_i];
    }
    var count = 0;
    var sumX = 0;
    var sumX2 = 0;
    stat_foreach(function (x) {
        count += 1;
        sumX += x;
        sumX2 += x * x;
    }, list);
    sumX2 /= count;
    sumX /= count;
    return sumX2 - sumX * sumX;
};
exports.functions.median = function () {
    var list = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        list[_i] = arguments[_i];
    }
    var values = [];
    stat_foreach(function (x) {
        values.push(x);
    }, list);
    values.sort(function (a, b) { return a - b; });
    if (values.length % 2 == 0) {
        return (values[values.length / 2] + values[values.length / 2 + 1]) / 2;
    }
    else {
        return values[(values.length - 1) / 2];
    }
};
exports.functions.avg = function () {
    var list = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        list[_i] = arguments[_i];
    }
    var r = 0, c = 0;
    stat_foreach(function (x) {
        r += x;
        c += 1;
    }, list);
    if (c == 0) {
        return NaN;
    }
    return r / c;
};
exports.functions.mean = exports.functions.avg;
exports.functions.average = exports.functions.avg;
exports.functions.quantile = function (q, list) {
    return quantile(q, list);
};
exports.functions.quartile1 = function () {
    var list = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        list[_i] = arguments[_i];
    }
    return quantile(0.25, list);
};
exports.functions.quartile3 = function () {
    var list = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        list[_i] = arguments[_i];
    }
    return quantile(0.75, list);
};
exports.functions.iqr = function () {
    var list = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        list[_i] = arguments[_i];
    }
    return quantile(0.75, list) - quantile(0.25, list);
};
// General operators
exports.operators["+"] = makeArrayCapable2(function (a, b) { return a + b; });
exports.operators["-"] = makeArrayCapable2(function (a, b) { return a - b; });
exports.operators["*"] = makeArrayCapable2(function (a, b) { return a * b; });
exports.operators["/"] = makeArrayCapable2(function (a, b) { return a / b; });
exports.operators["^"] = makeArrayCapable2(function (a, b) { return Math.pow(a, b); });
exports.operators["unary:+"] = makeArrayCapable1(function (a) { return +a; });
exports.operators["unary:-"] = makeArrayCapable1(function (a) { return -a; });
exports.operators["<"] = makeArrayCapable2(function (a, b) { return a < b; });
exports.operators[">"] = makeArrayCapable2(function (a, b) { return a > b; });
exports.operators["<="] = makeArrayCapable2(function (a, b) { return a <= b; });
exports.operators[">="] = makeArrayCapable2(function (a, b) { return a >= b; });
exports.operators["=="] = makeArrayCapable2(function (a, b) { return a == b; });
exports.operators["!="] = makeArrayCapable2(function (a, b) { return a != b; });
exports.operators.and = makeArrayCapable2(function (a, b) { return a && b; });
exports.operators.or = makeArrayCapable2(function (a, b) { return a || b; });
exports.operators["unary:not"] = makeArrayCapable1(function (a) { return !a; });
// Date operations
// TODO convert to class with static methods
// functions.date = {
//   parse: makeArrayCapable1((x: string) => {
//     debugger;
//     parseDate(x, isUtcTimeZone() ? 0 : new Date().getTimezoneOffset())
//   }),
//   year: makeArrayCapable1(utcFormat("%Y")), // year with century as a decimal number.
//   month: makeArrayCapable1(utcFormat("%b")), // month as a string "Jan" - "Dec".
//   monthnumber: makeArrayCapable1(utcFormat("%m")), // zero-padded number of the month as a decimal number [01,12].
//   day: makeArrayCapable1(utcFormat("%d")), // zero-padded day of the month as a decimal number [01,31].
//   weekOfYear: makeArrayCapable1(utcFormat("%U")), // Sunday-based week of the year as a decimal number [00,53].
//   dayOfYear: makeArrayCapable1(utcFormat("%j")), // day of the year as a decimal number [001,366].
//   weekday: makeArrayCapable1(utcFormat("%a")), // abbreviated weekday name.
//   hour: makeArrayCapable1(utcFormat("%H")), // hour (24-hour clock) as a decimal number [00,23].
//   minute: makeArrayCapable1(utcFormat("%M")), // minute as a decimal number [00,59].
//   second: makeArrayCapable1(utcFormat("%S")), // second as a decimal number [00,61].
//   timestamp: makeArrayCapable1((d: Date) => d.getTime() / 1000),
// };
var DateFunction = /** @class */ (function () {
    function DateFunction() {
    }
    Object.defineProperty(DateFunction.prototype, "hour", {
        get: function () {
            return makeArrayCapable1(common_1.isUtcTimeZone() ? d3_time_format_1.utcFormat("%H") : d3_time_format_1.timeFormat("%H"));
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DateFunction.prototype, "parse", {
        get: function () {
            return makeArrayCapable1(function (x) { return common_1.isUtcTimeZone() ? d3_time_format_1.utcParse(x) : datetime_1.parseDate(x); });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DateFunction.prototype, "year", {
        get: function () {
            return makeArrayCapable1(common_1.isUtcTimeZone() ? d3_time_format_1.utcFormat("%Y") : d3_time_format_1.timeFormat("%Y")); // year with century as a decimal number.
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DateFunction.prototype, "month", {
        get: function () {
            return makeArrayCapable1(common_1.isUtcTimeZone() ? d3_time_format_1.utcFormat("%b") : d3_time_format_1.timeFormat("%b")); // month as a string "Jan" - "Dec".
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DateFunction.prototype, "monthnumber", {
        get: function () {
            return makeArrayCapable1(common_1.isUtcTimeZone() ? d3_time_format_1.utcFormat("%m") : d3_time_format_1.timeFormat("%m")); // zero-padded number of the month as a decimal number [01,12].
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DateFunction.prototype, "day", {
        get: function () {
            return makeArrayCapable1(common_1.isUtcTimeZone() ? d3_time_format_1.utcFormat("%d") : d3_time_format_1.timeFormat("%d")); // zero-padded day of the month as a decimal number [01,31].
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DateFunction.prototype, "weekOfYear", {
        get: function () {
            return makeArrayCapable1(common_1.isUtcTimeZone() ? d3_time_format_1.utcFormat("%U") : d3_time_format_1.timeFormat("%U")); // Sunday-based week of the year as a decimal number [00,53].
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DateFunction.prototype, "dayOfYear", {
        get: function () {
            return makeArrayCapable1(common_1.isUtcTimeZone() ? d3_time_format_1.utcFormat("%j") : d3_time_format_1.timeFormat("%j")); // day of the year as a decimal number [001,366].
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DateFunction.prototype, "weekday", {
        get: function () {
            return makeArrayCapable1(common_1.isUtcTimeZone() ? d3_time_format_1.utcFormat("%a") : d3_time_format_1.timeFormat("%a")); // abbreviated weekday name.
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DateFunction.prototype, "minute", {
        get: function () {
            return makeArrayCapable1(common_1.isUtcTimeZone() ? d3_time_format_1.utcFormat("%M") : d3_time_format_1.timeFormat("%M")); // minute as a decimal number [00,59].
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DateFunction.prototype, "second", {
        get: function () {
            return makeArrayCapable1(common_1.isUtcTimeZone() ? d3_time_format_1.utcFormat("%S") : d3_time_format_1.timeFormat("%S")); // second as a decimal number [00,61].
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DateFunction.prototype, "timestamp", {
        get: function () {
            return makeArrayCapable1(function (d) { return d.getTime() / 1000; });
        },
        enumerable: false,
        configurable: true
    });
    return DateFunction;
}());
exports.functions.date = new DateFunction();
exports.functions.format = makeArrayCapable2(function (value, spec) {
    return common_1.getFormat()(spec)(value);
});
// JSON format
exports.functions.json = {
    parse: makeArrayCapable1(function (x) { return JSON.parse(x); }),
    stringify: makeArrayCapable1(function (x) { return JSON.stringify(x); }),
};
// Comparison
exports.functions.sortBy = function (fieldName, reversed) {
    if (reversed === void 0) { reversed = false; }
    var SM = reversed ? 1 : -1;
    var LG = reversed ? -1 : 1;
    if (typeof fieldName == "string") {
        return function (a, b) {
            var fa = a[fieldName];
            var fb = b[fieldName];
            if (fa == fb) {
                return 0;
            }
            return fa < fb ? SM : LG;
        };
    }
    else {
        return function (a, b) {
            var fa = fieldName(a);
            var fb = fieldName(b);
            if (fa == fb) {
                return 0;
            }
            return fa < fb ? SM : LG;
        };
    }
};
exports.functions.columnName = function (columns) {
    var names = [];
    for (var _i = 1; _i < arguments.length; _i++) {
        names[_i - 1] = arguments[_i];
    }
    if (columns instanceof Array) {
        return columns
            .filter(function (column) { return names.find(function (n) { return n == column.name; }); })
            .map(function (column) { return column.displayName || column.name; });
    }
    else {
        return columns.displayName || columns.name;
    }
};
//# sourceMappingURL=intrinsics.js.map