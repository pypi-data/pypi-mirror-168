"use strict";
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
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
var chai_1 = require("chai");
var datetime_1 = require("../../core/dataset/datetime");
var Expression = require("../../core/expression");
describe("Datetime Parser", function () {
    it("parseDate", function () {
        var e_1, _a;
        var cases = [
            // Date only
            ["2016-01", "2016-01-01T00:00:00.000Z", "Jan 2016 01 00 00"],
            ["01/2016", "2016-01-01T00:00:00.000Z", "Jan 2016 01 00 00"],
            ["2016-01-23", "2016-01-23T00:00:00.000Z", "Jan 2016 23 00 00"],
            ["01/23/2016", "2016-01-23T00:00:00.000Z", "Jan 2016 23 00 00"],
            // Date & Time
            ["01/23/2016  07:39:46", "2016-01-23T07:39:46.000Z", "Jan 2016 23 07 39"],
            ["01/23/2016  07:39", "2016-01-23T07:39:00.000Z", "Jan 2016 23 07 39"],
            // Date & Time (am/pm)
            [
                "2016-01-23   07:39:46am",
                "2016-01-23T07:39:46.000Z",
                "Jan 2016 23 07 39",
            ],
            [
                "2016-01-23 07:39:46pm",
                "2016-01-23T19:39:46.000Z",
                "Jan 2016 23 19 39",
            ],
            ["01/23/2016 12:03am", "2016-01-23T00:03:00.000Z", "Jan 2016 23 00 03"],
            ["01/23/2016 01:03am", "2016-01-23T01:03:00.000Z", "Jan 2016 23 01 03"],
            ["01/23/2016 01:03pm", "2016-01-23T13:03:00.000Z", "Jan 2016 23 13 03"],
            ["01/23/2016 12:03PM", "2016-01-23T12:03:00.000Z", "Jan 2016 23 12 03"],
            // Datetime & Timezone
            [
                "01/23/2016 12:03PM +01:34",
                "2016-01-23T13:37:00.000Z",
                "Jan 2016 23 13 37",
            ],
            [
                "01/23/2016 12:03PM -01:34",
                "2016-01-23T10:29:00.000Z",
                "Jan 2016 23 10 29",
            ],
            // ISO8601
            [
                "2016-05-24T15:54:14.876Z",
                "2016-05-24T15:54:14.876Z",
                "May 2016 24 15 54",
            ],
            ["2016-05-24T15:54:14Z", "2016-05-24T15:54:14.000Z", "May 2016 24 15 54"],
        ];
        try {
            for (var cases_1 = __values(cases), cases_1_1 = cases_1.next(); !cases_1_1.done; cases_1_1 = cases_1.next()) {
                var _b = __read(cases_1_1.value, 3), str = _b[0], datestr = _b[1], exprdatestr = _b[2];
                var r = datetime_1.parseDate(str, 0);
                var p = new Date(r).toISOString();
                chai_1.expect(p).to.equal(datestr, str);
                var ctx = new Expression.SimpleContext();
                ctx.variables.t = r;
                var expr = "${date.month(t)} ${date.year(t)} ${date.day(t)} ${date.hour(t)} ${date.minute(t)}";
                var parsed = Expression.parseTextExpression(expr);
                chai_1.expect(parsed.getValue(ctx)).to.equals(exprdatestr);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (cases_1_1 && !cases_1_1.done && (_a = cases_1.return)) _a.call(cases_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
    });
});
//# sourceMappingURL=datetime.js.map