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
exports.MarkSnappingSession = void 0;
var actions_1 = require("../../../actions");
var guides_1 = require("../../../../core/prototypes/guides");
var prototypes_1 = require("../../../../core/prototypes");
var session_1 = require("./session");
var specification_1 = require("../../../../core/specification");
var MarkSnappingSession = /** @class */ (function (_super) {
    __extends(MarkSnappingSession, _super);
    function MarkSnappingSession(guides, mark, element, elementState, bound, threshold, findClosestSnappingGuide) {
        var _this = _super.call(this, guides.filter(function (x) {
            // element cannot snap to itself
            if (x.element === element) {
                return false;
            }
            // special rules for guides
            if (element.classID === guides_1.GuideClass.classID) {
                // guide cannot snap to a mark
                if (x.element && prototypes_1.isType(x.element.classID, "mark")) {
                    return false;
                }
            }
            return true;
        }), bound, threshold, findClosestSnappingGuide) || this;
        _this.mark = mark;
        _this.element = element;
        return _this;
    }
    MarkSnappingSession.prototype.getActions = function (actions) {
        var e_1, _a;
        var g = new actions_1.Actions.MarkActionGroup();
        var updates = {};
        var hasUpdates = false;
        try {
            for (var actions_2 = __values(actions), actions_2_1 = actions_2.next(); !actions_2_1.done; actions_2_1 = actions_2.next()) {
                var action = actions_2_1.value;
                switch (action.type) {
                    case "snap":
                        {
                            if (action.snapElement == null) {
                                g.add(new actions_1.Actions.SetMarkAttribute(this.mark, this.element, action.attribute, {
                                    type: specification_1.MappingType.parent,
                                    parentAttribute: action.snapAttribute,
                                }));
                            }
                            else {
                                g.add(new actions_1.Actions.SnapMarks(this.mark, this.element, action.attribute, action.snapElement, action.snapAttribute));
                            }
                        }
                        break;
                    case "move":
                        {
                            updates[action.attribute] = action.value;
                            hasUpdates = true;
                        }
                        break;
                    case "property":
                        {
                            g.add(new actions_1.Actions.SetObjectProperty(this.element, action.property, action.field, action.value));
                        }
                        break;
                    case "value-mapping":
                        {
                            g.add(new actions_1.Actions.SetMarkAttribute(this.mark, this.element, action.attribute, {
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
        if (hasUpdates) {
            g.add(new actions_1.Actions.UpdateMarkAttribute(this.mark, this.element, updates));
        }
        // console.log(g);
        return g;
    };
    return MarkSnappingSession;
}(session_1.SnappingSession));
exports.MarkSnappingSession = MarkSnappingSession;
//# sourceMappingURL=mark.js.map