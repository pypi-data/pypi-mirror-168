import { VisualProperties, VisualUniforms, ValuesOf } from "./visual";
import { uint32 } from "../types";
import * as p from "../properties";
import * as mixins from "../property_mixins";
import { FontStyle, TextAlign, TextBaseline } from "../enums";
import { Context2d } from "../util/canvas";
export interface Text extends Readonly<mixins.Text> {
}
export declare class Text extends VisualProperties {
    get doit(): boolean;
    update(): void;
    Values: ValuesOf<mixins.Text>;
    values(): this["Values"];
    set_value(ctx: Context2d): void;
    font_value(): string;
}
export declare class TextScalar extends VisualUniforms {
    readonly text_color: p.UniformScalar<uint32>;
    readonly text_outline_color: p.UniformScalar<uint32>;
    readonly text_alpha: p.UniformScalar<number>;
    readonly text_font: p.UniformScalar<string>;
    readonly text_font_size: p.UniformScalar<string>;
    readonly text_font_style: p.UniformScalar<FontStyle>;
    readonly text_align: p.UniformScalar<TextAlign>;
    readonly text_baseline: p.UniformScalar<TextBaseline>;
    readonly text_line_height: p.UniformScalar<number>;
    get doit(): boolean;
    update(): void;
    Values: ValuesOf<mixins.Text>;
    values(): this["Values"];
    set_value(ctx: Context2d): void;
    font_value(): string;
}
export declare class TextVector extends VisualUniforms {
    readonly text_color: p.Uniform<uint32>;
    readonly text_outline_color: p.Uniform<uint32>;
    readonly text_alpha: p.Uniform<number>;
    readonly text_font: p.Uniform<string>;
    readonly text_font_size: p.Uniform<string>;
    readonly text_font_style: p.Uniform<FontStyle>;
    readonly text_align: p.Uniform<TextAlign>;
    readonly text_baseline: p.Uniform<TextBaseline>;
    readonly text_line_height: p.Uniform<number>;
    private _assert_font;
    Values: ValuesOf<mixins.Text>;
    values(i: number): this["Values"];
    get doit(): boolean;
    v_doit(i: number): boolean;
    apply(ctx: Context2d, i: number): boolean;
    set_vectorize(ctx: Context2d, i: number): void;
    font_value(i: number): string;
}
//# sourceMappingURL=text.d.ts.map