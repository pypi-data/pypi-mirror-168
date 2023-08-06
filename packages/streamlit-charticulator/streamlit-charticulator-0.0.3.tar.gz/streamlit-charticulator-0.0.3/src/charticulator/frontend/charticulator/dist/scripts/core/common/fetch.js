"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.loadDataFromURL = void 0;
function loadDataFromURL(url, contentType, 
// eslint-disable-next-line
timeout) {
    if (contentType === void 0) { contentType = "text"; }
    if (timeout === void 0) { timeout = 10; }
    return fetch(url).then(function (response) {
        if (response.ok && response.status == 200) {
            if (contentType == "text") {
                return response.text();
            }
            if (contentType == "json") {
                return response.json();
            }
            if (contentType == "arraybuffer") {
                return response.arrayBuffer();
            }
            if (contentType == "blob") {
                return response.blob();
            }
            return response.text();
        }
        else {
            throw new Error("failed to fetch url");
        }
    });
}
exports.loadDataFromURL = loadDataFromURL;
//# sourceMappingURL=fetch.js.map