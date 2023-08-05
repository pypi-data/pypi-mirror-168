import { Texture } from "./texture";
import * as p from "../../core/properties";
import { Color } from "../../core/types";
import { PatternSource } from "../../core/visuals/patterns";
export declare namespace CanvasTexture {
    type Attrs = p.AttrsOf<Props>;
    type Props = Texture.Props & {
        code: p.Property<string>;
    };
}
export interface CanvasTexture extends CanvasTexture.Attrs {
}
export declare abstract class CanvasTexture extends Texture {
    properties: CanvasTexture.Props;
    constructor(attrs?: Partial<CanvasTexture.Attrs>);
    get func(): Function;
    get_pattern(color: Color, scale: number, weight: number): PatternSource;
}
//# sourceMappingURL=canvas_texture.d.ts.map