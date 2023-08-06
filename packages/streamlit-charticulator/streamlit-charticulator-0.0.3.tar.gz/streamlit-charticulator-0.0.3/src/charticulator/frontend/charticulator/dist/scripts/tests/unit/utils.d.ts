import { AppStoreState } from "../../app/stores";
import { DefaultAttributes } from "../../core/prototypes";
export declare function makeDefaultAttributes(state: AppStoreState): DefaultAttributes;
/** Test if a deep equals b with tolerance on numeric values */
export declare function expect_deep_approximately_equals(a: any, b: any, tol: number, context?: any): void;
export declare function parseSVGTransform(a: any): any;
export declare const pathPrefix = "tests/unit/charts";
export declare function loadJSON(url: string): Promise<any>;
export declare function waitSolver(): Promise<void>;
