export declare function loadDataFromURL(url: string, contentType: "text", timeout?: number): Promise<string>;
export declare function loadDataFromURL(url: string, contentType: "json", timeout?: number): Promise<Record<string, unknown>>;
export declare function loadDataFromURL(url: string, contentType: "arraybuffer", timeout?: number): Promise<ArrayBuffer>;
export declare function loadDataFromURL(url: string, contentType: "blob", timeout?: number): Promise<Blob>;
