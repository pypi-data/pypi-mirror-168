import * as React from "react";
import { Prototypes } from "../../../../core";
import { CharticulatorPropertyAccessors } from "./types";
export declare const FilterPanel: React.FC<{
    text: string;
    options: Prototypes.Controls.FilterEditorOptions;
    manager: Prototypes.Controls.WidgetManager & CharticulatorPropertyAccessors;
}>;
