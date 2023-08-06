import { ItemData, ItemDescription, ItemMetadata } from "./abstract";
export declare function uuid(): string;
/** Responsible to manage saving, loading, storing charts created by user in IndexedDB of the browser */
export declare class IndexedDBBackend {
    private databaseName;
    private database;
    constructor(db?: string);
    open(): Promise<void>;
    list(type: string, orderBy?: string, start?: number, count?: number): Promise<{
        items: ItemDescription[];
        totalCount: number;
    }>;
    get(id: string): Promise<ItemData>;
    put(id: string, data: any, metadata?: ItemMetadata): Promise<void>;
    create(type: string, data: any, metadata?: ItemMetadata): Promise<string>;
    delete(id: string): Promise<void>;
}
