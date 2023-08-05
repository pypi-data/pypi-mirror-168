import { BaseGLGlyph } from "./base";
import { Float32Buffer, Uint8Buffer } from "./buffer";
import { cap_lookup, join_lookup } from "./webgl_utils";
import { color2rgba } from "../../../core/util/color";
import { resolve_line_dash } from "../../../core/visuals/line";
export class BaseLineGL extends BaseGLGlyph {
    constructor(regl_wrapper, glyph) {
        super(regl_wrapper, glyph);
        this.glyph = glyph;
        this._antialias = 1.5; // Make this larger to test antialiasing at edges.
        this._miter_limit = 5.0; // Threshold for miters to be replaced by bevels.
    }
    _draw_impl(transform, main_gl_glyph) {
        if (this.visuals_changed) {
            this._set_visuals();
            this.visuals_changed = false;
        }
        if (main_gl_glyph.data_changed) {
            main_gl_glyph._set_data();
            main_gl_glyph.data_changed = false;
        }
        const line_visuals = this._get_visuals().line;
        const line_cap = cap_lookup[line_visuals.line_cap.value];
        const line_join = join_lookup[line_visuals.line_join.value];
        const points = main_gl_glyph._points;
        const solid_props = {
            scissor: this.regl_wrapper.scissor,
            viewport: this.regl_wrapper.viewport,
            canvas_size: [transform.width, transform.height],
            pixel_ratio: transform.pixel_ratio,
            line_color: this._color,
            linewidth: this._linewidth,
            antialias: this._antialias,
            miter_limit: this._miter_limit,
            points,
            show: main_gl_glyph._show,
            nsegments: points.length / 2 - 3,
            line_join,
            line_cap,
        };
        if (this._is_dashed()) {
            const dashed_props = {
                ...solid_props,
                length_so_far: this._length_so_far,
                dash_tex: this._dash_tex,
                dash_tex_info: this._dash_tex_info,
                dash_scale: this._dash_scale,
                dash_offset: this._dash_offset,
            };
            this.regl_wrapper.dashed_line()(dashed_props);
        }
        else {
            this.regl_wrapper.solid_line()(solid_props);
        }
    }
    _is_dashed() {
        return this._line_dash.length > 0;
    }
    _set_data() {
        const points_array = this._set_data_points();
        // Points array includes extra points at each end
        const npoints = points_array.length / 2 - 2;
        if (this._show == null)
            this._show = new Uint8Buffer(this.regl_wrapper);
        const show_array = this._show.get_sized_array(npoints + 1);
        let start_finite = isFinite(points_array[2]) && isFinite(points_array[3]);
        for (let i = 1; i < npoints; i++) {
            const end_finite = isFinite(points_array[2 * i + 2]) && isFinite(points_array[2 * i + 3]);
            show_array[i] = (start_finite && end_finite) ? 1 : 0;
            start_finite = end_finite;
        }
        if (this._is_closed) {
            show_array[0] = show_array[npoints - 1];
            show_array[npoints] = show_array[1];
        }
        else {
            show_array[0] = 0;
            show_array[npoints] = 0;
        }
        this._show.update();
        if (this._is_dashed()) {
            const nsegments = npoints - 1;
            if (this._length_so_far == null)
                this._length_so_far = new Float32Buffer(this.regl_wrapper);
            const lengths_array = this._length_so_far.get_sized_array(nsegments);
            let length = 0.0;
            for (let i = 0; i < nsegments; i++) {
                lengths_array[i] = length;
                if (show_array[i + 1] == 1)
                    length += Math.sqrt((points_array[2 * i + 4] - points_array[2 * i + 2]) ** 2 +
                        (points_array[2 * i + 5] - points_array[2 * i + 3]) ** 2);
            }
            this._length_so_far.update();
        }
    }
    _set_visuals() {
        const line_visuals = this._get_visuals().line;
        const color = color2rgba(line_visuals.line_color.value, line_visuals.line_alpha.value);
        this._color = color.map((val) => val / 255);
        this._linewidth = line_visuals.line_width.value;
        if (this._linewidth < 1.0) {
            // Linewidth less than 1 is implemented as 1 but with reduced alpha.
            this._color[3] *= this._linewidth;
            this._linewidth = 1.0;
        }
        this._line_dash = resolve_line_dash(line_visuals.line_dash.value);
        if (this._is_dashed()) {
            [this._dash_tex_info, this._dash_tex, this._dash_scale] =
                this.regl_wrapper.get_dash(this._line_dash);
            this._dash_offset = line_visuals.line_dash_offset.value;
        }
    }
}
BaseLineGL.__name__ = "BaseLineGL";
//# sourceMappingURL=base_line.js.map