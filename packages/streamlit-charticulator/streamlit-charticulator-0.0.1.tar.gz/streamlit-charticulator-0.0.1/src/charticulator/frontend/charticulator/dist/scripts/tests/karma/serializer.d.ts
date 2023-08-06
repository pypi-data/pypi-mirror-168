/// <reference types="chai" />
import ChaiUtils = Chai.ChaiUtils;
import ChaiStatic = Chai.ChaiStatic;
export declare function matchSnapshot(chai: ChaiStatic, utils: ChaiUtils): void;
declare global {
    namespace Chai {
        interface Assertion {
            matchSnapshot(lang?: any, update?: boolean): Assertion;
        }
        interface AssertStatic {
            matchSnapshot(lang?: any, update?: boolean): Assertion;
        }
    }
}
