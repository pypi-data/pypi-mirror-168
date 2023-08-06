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
exports.ChartSnappingSession = void 0;
var specification_1 = require("../../../../core/specification");
var actions_1 = require("../../../actions");
var session_1 = require("./session");
var ChartSnappingSession = /** @class */ (function (_super) {
    __extends(ChartSnappingSession, _super);
    function ChartSnappingSession(guides, markLayout, bound, threshold, findClosestSnappingGuide) {
        var _this = _super.call(this, guides.filter(function (x) { return x.element != markLayout; }), bound, threshold, findClosestSnappingGuide) || this;
        _this.markLayout = markLayout;
        return _this;
    }
    ChartSnappingSession.prototype.getActions = function (actions) {
        var e_1, _a;
        var result = [];
        try {
            for (var actions_2 = __values(actions), actions_2_1 = actions_2.next(); !actions_2_1.done; actions_2_1 = actions_2.next()) {
                var action = actions_2_1.value;
                switch (action.type) {
                    case "snap":
                        {
                            if (action.snapElement == null) {
                                result.push(new actions_1.Actions.SetChartElementMapping(this.markLayout, action.attribute, {
                                    type: specification_1.MappingType.parent,
                                    parentAttribute: action.snapAttribute,
                                }));
                            }
                            else {
                                result.push(new actions_1.Actions.SnapChartElements(this.markLayout, action.attribute, action.snapElement, action.snapAttribute));
                            }
                        }
                        break;
                    case "move":
                        {
                            var updates = {};
                            updates[action.attribute] = action.value;
                            result.push(new actions_1.Actions.UpdateChartElementAttribute(this.markLayout, updates));
                        }
                        break;
                    case "property":
                        {
                            result.push(new actions_1.Actions.SetObjectProperty(this.markLayout, action.property, action.field, action.value));
                        }
                        break;
                    case "value-mapping":
                        {
                            result.push(new actions_1.Actions.SetChartElementMapping(this.markLayout, action.attribute, {
                                type: specification_1.MappingType.value,
                                value: action.value,
                            }));
                        }
                        break;
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (actions_2_1 && !actions_2_1.done && (_a = actions_2.return)) _a.call(actions_2);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return result;
    };
    return ChartSnappingSession;
}(session_1.SnappingSession));
exports.ChartSnappingSession = ChartSnappingSession;
//# sourceMappingURL=chart.js.map