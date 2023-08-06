"use strict";
/**
 * @ignore
 * @packageDocumentation
 * @preferred
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.getConfig = exports.setConfig = void 0;
var config;
function setConfig(_) {
    if (_ == null) {
        config = {};
    }
    else {
        config = _;
    }
}
exports.setConfig = setConfig;
function getConfig() {
    return config;
}
exports.getConfig = getConfig;
//# sourceMappingURL=config.js.map