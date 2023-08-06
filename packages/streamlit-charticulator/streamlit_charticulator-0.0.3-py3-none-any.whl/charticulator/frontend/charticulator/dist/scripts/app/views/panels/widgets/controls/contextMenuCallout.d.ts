/// <reference types="react" />
import { AppStore } from "../../../../../app/stores";
interface ContextMenuCalloutProps {
    store?: AppStore;
    calloutId: string;
    hideCallout: (value: boolean) => void;
    calloutVisible: boolean;
}
export declare const ContextMenuCallout: ({ store, calloutId, hideCallout, calloutVisible, }: ContextMenuCalloutProps) => JSX.Element;
export {};
