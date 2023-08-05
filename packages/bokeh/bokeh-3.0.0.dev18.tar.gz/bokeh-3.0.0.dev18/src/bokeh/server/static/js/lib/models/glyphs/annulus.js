var _a;
import { XYGlyph, XYGlyphView } from "./xy_glyph";
import { to_screen } from "../../core/types";
import { LineVector, FillVector, HatchVector } from "../../core/property_mixins";
import * as p from "../../core/properties";
import { Selection } from "../selections/selection";
export class AnnulusView extends XYGlyphView {
    _map_data() {
        if (this.model.properties.inner_radius.units == "data")
            this.sinner_radius = this.sdist(this.renderer.xscale, this._x, this.inner_radius);
        else
            this.sinner_radius = to_screen(this.inner_radius);
        if (this.model.properties.outer_radius.units == "data")
            this.souter_radius = this.sdist(this.renderer.xscale, this._x, this.outer_radius);
        else
            this.souter_radius = to_screen(this.outer_radius);
    }
    _render(ctx, indices, data) {
        const { sx, sy, sinner_radius, souter_radius } = data ?? this;
        for (const i of indices) {
            const sx_i = sx[i];
            const sy_i = sy[i];
            const sinner_radius_i = sinner_radius[i];
            const souter_radius_i = souter_radius[i];
            if (!isFinite(sx_i + sy_i + sinner_radius_i + souter_radius_i))
                continue;
            ctx.beginPath();
            ctx.arc(sx_i, sy_i, sinner_radius_i, 0, 2 * Math.PI, true);
            ctx.moveTo(sx_i + souter_radius_i, sy_i);
            ctx.arc(sx_i, sy_i, souter_radius_i, 2 * Math.PI, 0, false);
            this.visuals.fill.apply(ctx, i);
            this.visuals.hatch.apply(ctx, i);
            this.visuals.line.apply(ctx, i);
        }
    }
    _hit_point(geometry) {
        const { sx, sy } = geometry;
        const x = this.renderer.xscale.invert(sx);
        const y = this.renderer.yscale.invert(sy);
        let x0, y0;
        let x1, y1;
        if (this.model.properties.outer_radius.units == "data") {
            x0 = x - this.max_outer_radius;
            x1 = x + this.max_outer_radius;
            y0 = y - this.max_outer_radius;
            y1 = y + this.max_outer_radius;
        }
        else {
            const sx0 = sx - this.max_outer_radius;
            const sx1 = sx + this.max_outer_radius;
            [x0, x1] = this.renderer.xscale.r_invert(sx0, sx1);
            const sy0 = sy - this.max_outer_radius;
            const sy1 = sy + this.max_outer_radius;
            [y0, y1] = this.renderer.yscale.r_invert(sy0, sy1);
        }
        const indices = [];
        for (const i of this.index.indices({ x0, x1, y0, y1 })) {
            const or2 = this.souter_radius[i] ** 2;
            const ir2 = this.sinner_radius[i] ** 2;
            const [sx0, sx1] = this.renderer.xscale.r_compute(x, this._x[i]);
            const [sy0, sy1] = this.renderer.yscale.r_compute(y, this._y[i]);
            const dist = (sx0 - sx1) ** 2 + (sy0 - sy1) ** 2;
            if (dist <= or2 && dist >= ir2)
                indices.push(i);
        }
        return new Selection({ indices });
    }
    draw_legend_for_index(ctx, { x0, y0, x1, y1 }, index) {
        const len = index + 1;
        const sx = new Array(len);
        sx[index] = (x0 + x1) / 2;
        const sy = new Array(len);
        sy[index] = (y0 + y1) / 2;
        const r = Math.min(Math.abs(x1 - x0), Math.abs(y1 - y0)) * 0.5;
        const sinner_radius = new Array(len);
        sinner_radius[index] = r * 0.4;
        const souter_radius = new Array(len);
        souter_radius[index] = r * 0.8;
        this._render(ctx, [index], { sx, sy, sinner_radius, souter_radius }); // XXX
    }
}
AnnulusView.__name__ = "AnnulusView";
export class Annulus extends XYGlyph {
    constructor(attrs) {
        super(attrs);
    }
}
_a = Annulus;
Annulus.__name__ = "Annulus";
(() => {
    _a.prototype.default_view = AnnulusView;
    _a.mixins([LineVector, FillVector, HatchVector]);
    _a.define(({}) => ({
        inner_radius: [p.DistanceSpec, { field: "inner_radius" }],
        outer_radius: [p.DistanceSpec, { field: "outer_radius" }],
    }));
})();
//# sourceMappingURL=annulus.js.map