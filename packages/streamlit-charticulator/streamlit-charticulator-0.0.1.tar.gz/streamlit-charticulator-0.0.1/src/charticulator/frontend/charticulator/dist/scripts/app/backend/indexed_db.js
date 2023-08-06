"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.IndexedDBBackend = exports.uuid = void 0;
function s4() {
    // eslint-disable-next-line
    return Math.floor((1 + Math.random()) * 0x10000)
        .toString(16)
        .substring(1);
}
function uuid() {
    return (s4() +
        s4() +
        "-" +
        s4() +
        "-" +
        s4() +
        "-" +
        s4() +
        "-" +
        s4() +
        s4() +
        s4());
}
exports.uuid = uuid;
/** Responsible to manage saving, loading, storing charts created by user in IndexedDB of the browser */
var IndexedDBBackend = /** @class */ (function () {
    function IndexedDBBackend(db) {
        if (db === void 0) { db = "charticulator"; }
        this.databaseName = db;
        this.database = null;
    }
    IndexedDBBackend.prototype.open = function () {
        var _this = this;
        return new Promise(function (resolve, reject) {
            if (_this.database) {
                resolve();
            }
            else {
                var request_1 = indexedDB.open(_this.databaseName, 2);
                request_1.onupgradeneeded = function () {
                    _this.database = request_1.result;
                    var itemsStore = _this.database.createObjectStore("items", {
                        keyPath: "id",
                    });
                    itemsStore.createIndex("TypeIndex", "type");
                    itemsStore.createIndex("DataIDIndex", "dataID");
                    itemsStore.createIndex("NameIndex", "metadata.name");
                    itemsStore.createIndex("TimeCreatedIndex", "metadata.timeCreated");
                    itemsStore.createIndex("TimeModifiedIndex", "metadata.timeModified");
                    _this.database.createObjectStore("data", {
                        keyPath: "id",
                    });
                };
                request_1.onerror = function () {
                    reject(new Error("could not open database"));
                };
                request_1.onsuccess = function () {
                    _this.database = request_1.result;
                    resolve();
                };
            }
        });
    };
    IndexedDBBackend.prototype.list = function (type, orderBy, start, count) {
        var _this = this;
        if (orderBy === void 0) { orderBy = "timeCreated"; }
        if (start === void 0) { start = 0; }
        if (count === void 0) { count = 50; }
        return this.open().then(function () {
            return new Promise(function (resolve, reject) {
                var tx = _this.database.transaction("items", "readonly");
                var store = tx.objectStore("items");
                var request = store.index("TypeIndex").openCursor(type);
                var result = [];
                request.onsuccess = function () {
                    var cursor = request.result;
                    if (cursor) {
                        var value = cursor.value;
                        result.push(value);
                        cursor.continue();
                    }
                    else {
                        var resultFiltered = result.sort(function (a, b) {
                            return b.metadata[orderBy] - a.metadata[orderBy];
                        });
                        resultFiltered = resultFiltered.slice(start, start + count);
                        resolve({
                            items: resultFiltered,
                            totalCount: result.length,
                        });
                    }
                };
                request.onerror = function () {
                    reject(new Error("could not read from the database"));
                };
            });
        });
    };
    IndexedDBBackend.prototype.get = function (id) {
        var _this = this;
        return this.open().then(function () {
            return new Promise(function (resolve, reject) {
                var tx = _this.database.transaction(["items", "data"], "readonly");
                var itemsStore = tx.objectStore("items");
                var dataStore = tx.objectStore("data");
                var request = itemsStore.get(id);
                request.onsuccess = function () {
                    var item = request.result;
                    var request2 = dataStore.get(item.dataID);
                    request2.onsuccess = function () {
                        item.data = request2.result.data;
                        resolve(item);
                    };
                    request2.onerror = function () {
                        reject(new Error("could not read from the database"));
                    };
                };
                request.onerror = function () {
                    reject(new Error("could not read from the database"));
                };
            });
        });
    };
    IndexedDBBackend.prototype.put = function (id, data, metadata) {
        var _this = this;
        return this.open().then(function () {
            return new Promise(function (resolve, reject) {
                var tx = _this.database.transaction(["items", "data"], "readwrite");
                var itemsStore = tx.objectStore("items");
                var dataStore = tx.objectStore("data");
                var req1 = itemsStore.get(id);
                req1.onerror = function () {
                    reject(new Error("could not write to the database"));
                };
                req1.onsuccess = function () {
                    var original = req1.result;
                    metadata.timeCreated = original.metadata.timeCreated;
                    metadata.timeModified = new Date().getTime();
                    var obj = {
                        id: id,
                        dataID: req1.result.dataID,
                        type: original.type,
                        metadata: metadata,
                    };
                    var dataObj = {
                        id: req1.result.dataID,
                        data: data,
                    };
                    dataStore.put(dataObj);
                    itemsStore.put(obj);
                    tx.oncomplete = function () {
                        resolve();
                    };
                    tx.onerror = function () {
                        reject(new Error("could not write to the database"));
                    };
                };
            });
        });
    };
    IndexedDBBackend.prototype.create = function (type, data, metadata) {
        var _this = this;
        return this.open().then(function () {
            return new Promise(function (resolve, reject) {
                var tx = _this.database.transaction(["items", "data"], "readwrite");
                var itemsStore = tx.objectStore("items");
                var dataStore = tx.objectStore("data");
                metadata.timeCreated = new Date().getTime();
                metadata.timeModified = metadata.timeCreated;
                var obj = {
                    id: uuid(),
                    dataID: uuid(),
                    type: type,
                    metadata: metadata,
                };
                var dataObj = {
                    id: obj.dataID,
                    data: data,
                };
                dataStore.put(dataObj);
                itemsStore.put(obj);
                tx.oncomplete = function () {
                    resolve(obj.id);
                };
                tx.onerror = function () {
                    reject(new Error("could not write to the database"));
                };
            });
        });
    };
    IndexedDBBackend.prototype.delete = function (id) {
        var _this = this;
        return this.open().then(function () {
            return new Promise(function (resolve, reject) {
                var tx = _this.database.transaction(["items", "data"], "readwrite");
                var itemsStore = tx.objectStore("items");
                var dataStore = tx.objectStore("data");
                var request = itemsStore.get(id);
                request.onsuccess = function () {
                    var dataID = request.result.dataID;
                    itemsStore.delete(id);
                    dataStore.delete(dataID);
                    tx.oncomplete = function () {
                        resolve();
                    };
                    tx.onerror = function () {
                        reject(new Error("could not write to the database"));
                    };
                };
                request.onerror = function () {
                    reject(new Error("could not write to the database"));
                };
            });
        });
    };
    return IndexedDBBackend;
}());
exports.IndexedDBBackend = IndexedDBBackend;
//# sourceMappingURL=indexed_db.js.map