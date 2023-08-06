/**
 * Core part has two actions {@link SelectMark} and {@link ClearSelection}.
 *
 * {@link SelectMark} dispatches on selection
 *
 * {@link ClearSelection} dispatches on reset selection
 *
 * {@link Action} is base class for actions
 *
 * @packageDocumentation
 * @preferred
 */
import { Dispatcher } from "../common";
import { Glyph, Element, PlotSegment } from "../specification";
import * as Specification from "../specification";
export declare function objectDigest(obj?: Specification.Object): string[];
/**
 * Base class for all actions to describe all user interactions with charticulators objects
 * Actions dispatches by {@link BaseStore.dispatcher} method of the store.
 * List of charticulator app actions can be found in {@link "app/actions/actions"} module
 */
export declare class Action {
    dispatch(dispatcher: Dispatcher<Action>): void;
    digest(): {
        name: string;
    };
}
/** Dispatches when user selects the mark on the chart */
export declare class SelectMark extends Action {
    plotSegment: PlotSegment;
    glyph: Glyph;
    mark: Element;
    glyphIndex: number;
    /**
     * @param plotSegment plot segment where mark was selected
     * @param glyph glyph where mark was selected (on a glyph editor or on a chart)
     * @param mark selected mark
     * @param glyphIndex index of glyph
     */
    constructor(plotSegment: PlotSegment, glyph: Glyph, mark: Element, glyphIndex?: number);
    digest(): {
        name: string;
        plotSegment: string[];
        glyph: string[];
        mark: string[];
        glyphIndex: number;
    };
}
/** Dispatches when user reset selection of the mark on the chart */
export declare class ClearSelection extends Action {
    digest(): {
        name: string;
    };
}
