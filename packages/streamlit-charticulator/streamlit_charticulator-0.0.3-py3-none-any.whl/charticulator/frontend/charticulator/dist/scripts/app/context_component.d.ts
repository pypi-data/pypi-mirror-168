import * as React from "react";
import { AppStore } from "./stores";
import { Action } from "./actions/actions";
export interface MainContextInterface {
    store: AppStore;
}
export declare const MainContextTypes: {
    store: (props: any, propName: string, componentName: string) => Error;
};
export declare class ContextedComponent<TProps, TState> extends React.Component<TProps, TState> {
    context: MainContextInterface;
    constructor(props: TProps, context: MainContextInterface);
    static contextTypes: {
        store: (props: any, propName: string, componentName: string) => Error;
    };
    dispatch(action: Action): void;
    get store(): AppStore;
}
export declare const MainReactContext: React.Context<MainContextInterface>;
