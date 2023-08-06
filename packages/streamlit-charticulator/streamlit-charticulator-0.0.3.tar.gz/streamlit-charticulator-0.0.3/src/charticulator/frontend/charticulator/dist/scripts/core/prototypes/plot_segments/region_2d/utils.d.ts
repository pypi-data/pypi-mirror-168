import { PolarAttributes, PolarProperties } from "./polar";
export declare enum SIDE {
    HORIZONTAL = 0,
    VERTICAL = 1,
    NONE = 2
}
interface CenterType {
    cx: number;
    cy: number;
    side: SIDE;
    isHalf: boolean;
    isRightHalf: boolean;
    isCorner: boolean;
}
export declare function getCenterByAngle(properties: PolarProperties, attrs: PolarAttributes): CenterType;
export declare function getHandlesRadius(props: PolarProperties, attrs: PolarAttributes, center: CenterType): number;
export declare function setRadiiByCenter(props: PolarProperties, attrs: PolarAttributes, center: CenterType): void;
export declare function getRadialAxisDropZoneLineCenter(center: CenterType, radial1: number, radial2: number): {
    p1: {
        x: number;
        y: number;
    };
    p2: {
        x: number;
        y: number;
    };
};
export {};
