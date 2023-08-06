import { ColorPalette } from "../../resources";
import * as React from "react";
export interface PaletteListProps {
    selected: ColorPalette;
    palettes: ColorPalette[];
    onClick?: (palette: ColorPalette) => void;
}
export declare class PaletteList extends React.PureComponent<PaletteListProps, Record<string, unknown>> {
    render(): JSX.Element;
}
