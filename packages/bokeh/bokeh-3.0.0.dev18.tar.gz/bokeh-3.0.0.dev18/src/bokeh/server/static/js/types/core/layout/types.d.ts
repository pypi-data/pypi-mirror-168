import { Align } from "../enums";
import { Size, Extents } from "../types";
export { Size };
import { LRTB } from "../util/bbox";
export declare class Sizeable implements Size {
    width: number;
    height: number;
    constructor(size?: Partial<Size>);
    bounded_to({ width, height }: Partial<Size>): Sizeable;
    expanded_to({ width, height }: Size): Sizeable;
    expand_to({ width, height }: Size): void;
    narrowed_to({ width, height }: Size): Sizeable;
    narrow_to({ width, height }: Size): void;
    grow_by({ left, right, top, bottom }: Extents): Sizeable;
    shrink_by({ left, right, top, bottom }: Extents): Sizeable;
    map(w_fn: (v: number) => number, h_fn?: (v: number) => number): Sizeable;
}
export declare type Margin = Extents;
export declare type SizeHint = Size & {
    inner?: Extents;
    align?: LRTB<boolean> & {
        fixed_width?: boolean;
        fixed_height?: boolean;
    };
};
export declare type SizingPolicy = "fixed" | "fit" | "min" | "max";
export declare const SizingPolicy: import("../kinds").Kinds.Enum<"fixed" | "max" | "min" | "fit">;
export declare type Sizing = number | "fit" | "min" | "max";
export declare type Percent = {
    percent: number;
};
export declare type BoxSizing = {
    width_policy: SizingPolicy;
    min_width?: number | Percent;
    width?: number;
    max_width?: number | Percent;
    height_policy: SizingPolicy;
    min_height?: number | Percent;
    height?: number;
    max_height?: number | Percent;
    aspect?: number;
    margin: Margin;
    visible: boolean;
    halign?: Align;
    valign?: Align;
};
//# sourceMappingURL=types.d.ts.map