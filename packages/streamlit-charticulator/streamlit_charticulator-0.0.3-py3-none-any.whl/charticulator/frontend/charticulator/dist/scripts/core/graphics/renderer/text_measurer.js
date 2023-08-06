"use strict";
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.
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
exports.splitByWidth = exports.split = exports.BREAKERS_REGEX = exports.SPACE = exports.TextMeasurer = void 0;
var __1 = require("../..");
var defaults_1 = require("../../../app/stores/defaults");
var TextMeasurer = /** @class */ (function () {
    function TextMeasurer() {
        if (typeof document != "undefined") {
            this.canvas = document.createElement("canvas");
            this.context = this.canvas.getContext("2d");
            this.fontFamily = defaults_1.defaultFont;
            this.fontSize = defaults_1.defaultFontSize;
        }
    }
    TextMeasurer.prototype.setFontFamily = function (family) {
        this.fontFamily = family;
    };
    TextMeasurer.prototype.setFontSize = function (size) {
        this.fontSize = size;
    };
    TextMeasurer.prototype.measure = function (text) {
        this.context.font = this.fontSize + "px \"" + this.fontFamily + "\"";
        return {
            width: this.context.measureText(text).width,
            fontSize: this.fontSize,
            ideographicBaseline: this.fontSize * TextMeasurer.parameters.ideographicBaseline[0] +
                TextMeasurer.parameters.ideographicBaseline[1],
            hangingBaseline: this.fontSize * TextMeasurer.parameters.hangingBaseline[0] +
                TextMeasurer.parameters.hangingBaseline[1],
            alphabeticBaseline: this.fontSize * TextMeasurer.parameters.alphabeticBaseline[0] +
                TextMeasurer.parameters.alphabeticBaseline[1],
            middle: this.fontSize * TextMeasurer.parameters.middle[0] +
                TextMeasurer.parameters.middle[1],
        };
    };
    TextMeasurer.GetGlobalInstance = function () {
        if (this.globalInstance == null) {
            this.globalInstance = new TextMeasurer();
        }
        return this.globalInstance;
    };
    TextMeasurer.Measure = function (text, family, size) {
        var inst = this.GetGlobalInstance();
        inst.setFontFamily(family);
        inst.setFontSize(size);
        return inst.measure(text);
    };
    TextMeasurer.ComputeTextPosition = function (x, y, metrics, alignX, alignY, xMargin, yMargin) {
        if (alignX === void 0) { alignX = "left"; }
        if (alignY === void 0) { alignY = "middle"; }
        if (xMargin === void 0) { xMargin = 0; }
        if (yMargin === void 0) { yMargin = 0; }
        var cwidth = metrics.width;
        var cheight = (metrics.middle - metrics.ideographicBaseline) * 2;
        var cx = cwidth / 2, cy = cheight / 2;
        if (alignX == "left") {
            cx = -xMargin;
        }
        if (alignX == "right") {
            cx = cwidth + xMargin;
        }
        if (alignY == "top") {
            cy = -yMargin;
        }
        if (alignY == "bottom") {
            cy = cheight + yMargin;
        }
        return [x - cx, y - cheight + cy - metrics.ideographicBaseline];
    };
    TextMeasurer.parameters = {
        hangingBaseline: [0.7245381636743151, -0.005125313493913097],
        ideographicBaseline: [-0.2120442632498544, 0.008153756552125913],
        alphabeticBaseline: [0, 0],
        middle: [0.34642399534071056, -0.22714036109493208],
    };
    TextMeasurer.globalInstance = null;
    return TextMeasurer;
}());
exports.TextMeasurer = TextMeasurer;
exports.SPACE = " ";
exports.BREAKERS_REGEX = /[\s]+/g;
function split(str) {
    return str.split(exports.BREAKERS_REGEX);
}
exports.split = split;
/**
 * Splits text to fragments do display text with word wrap
 * Source code taken from https://github.com/microsoft/powerbi-visuals-utils-formattingutils/blob/master/src/wordBreaker.ts#L130
 * @param content source of text
 * @param maxWidth max available with for text
 * @param maxNumLines limit lines count, rest of words will be drew in the last line
 * @param fontFamily font family
 * @param fontSize font size in px
 */
function splitByWidth(content, maxWidth, maxNumLines, fontFamily, fontSize) {
    // Default truncator returns string as-is
    var e_1, _a;
    var result = [];
    var words = split(content);
    var usedWidth = 0;
    var wordsInLine = [];
    try {
        for (var words_1 = __values(words), words_1_1 = words_1.next(); !words_1_1.done; words_1_1 = words_1.next()) {
            var word = words_1_1.value;
            // Last line? Just add whatever is left
            if (maxNumLines > 0 && result.length >= maxNumLines - 1) {
                wordsInLine.push(word);
                continue;
            }
            // Determine width if we add this word
            // Account for SPACE we will add when joining...
            var metrics = __1.Graphics.TextMeasurer.Measure(word, fontFamily, fontSize);
            var wordWidth = metrics.width;
            // If width would exceed max width,
            // then push used words and start new split result
            if (usedWidth + wordWidth > maxWidth) {
                // Word alone exceeds max width, just add it.
                if (wordsInLine.length === 0) {
                    result.push(word);
                    usedWidth = 0;
                    wordsInLine = [];
                    continue;
                }
                result.push(wordsInLine.join(exports.SPACE));
                usedWidth = 0;
                wordsInLine = [];
            }
            // ...otherwise, add word and continue
            wordsInLine.push(word);
            usedWidth += wordWidth;
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (words_1_1 && !words_1_1.done && (_a = words_1.return)) _a.call(words_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    // Push remaining words onto result (if any)
    if (wordsInLine && wordsInLine.length) {
        result.push(wordsInLine.join(exports.SPACE));
    }
    return result;
}
exports.splitByWidth = splitByWidth;
//# sourceMappingURL=text_measurer.js.map