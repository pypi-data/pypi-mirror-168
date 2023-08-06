/**
 * The page side of the work instance, handles RPC and Tasks
 */
export declare class WorkerRPC {
    private worker;
    private currentUniqueID;
    private idCallbacks;
    constructor(workerScriptURL: string);
    private newUniqueID;
    rpc(path: string, ...args: any[]): Promise<any>;
}
export declare class WorkerHostProcess {
    private rpcMethods;
    constructor();
    registerRPC(path: string, method: (...args: any) => void | Promise<any>): void;
    private handleMessage;
}
