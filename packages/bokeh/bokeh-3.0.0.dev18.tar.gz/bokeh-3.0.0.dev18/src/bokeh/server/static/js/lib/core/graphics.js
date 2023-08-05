import { BBox } from "./util/bbox";
import { font_metrics, parse_css_font_size } from "./util/text";
import { max, max_by, sum } from "./util/array";
import { isNumber } from "./util/types";
import { AffineTransform } from "./util/affine";
import { color2css } from "./util/color";
export const text_width = (() => {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    let current_font = "";
    return (text, font) => {
        if (font != current_font) {
            current_font = font;
            ctx.font = font;
        }
        return ctx.measureText(text).width;
    };
})();
export class GraphicsBox {
    constructor() {
        this._position = { sx: 0, sy: 0 };
        this.font_size_scale = 1.0;
        this.align = "left";
        this._base_font_size = 13; // the same as :host's font-size (13px)
        this._x_anchor = "left";
        this._y_anchor = "center";
    }
    set base_font_size(v) {
        if (v != null)
            this._base_font_size = v;
    }
    get base_font_size() {
        return this._base_font_size;
    }
    set position(p) {
        this._position = p;
    }
    get position() {
        return this._position;
    }
    infer_text_height() {
        return "ascent_descent";
    }
    bbox() {
        const { p0, p1, p2, p3 } = this.rect();
        const left = Math.min(p0.x, p1.x, p2.x, p3.x);
        const top = Math.min(p0.y, p1.y, p2.y, p3.y);
        const right = Math.max(p0.x, p1.x, p2.x, p3.x);
        const bottom = Math.max(p0.y, p1.y, p2.y, p3.y);
        return new BBox({ left, right, top, bottom });
    }
    size() {
        const { width, height } = this._size();
        const { angle } = this;
        if (angle == null || angle == 0)
            return { width, height };
        else {
            const c = Math.cos(Math.abs(angle));
            const s = Math.sin(Math.abs(angle));
            return {
                width: Math.abs(width * c + height * s),
                height: Math.abs(width * s + height * c),
            };
        }
    }
    rect() {
        const rect = this._rect();
        const { angle } = this;
        if (angle == null || angle == 0)
            return rect;
        else {
            const { sx, sy } = this.position;
            const tr = new AffineTransform();
            tr.translate(sx, sy);
            tr.rotate(angle);
            tr.translate(-sx, -sy);
            return tr.apply_rect(rect);
        }
    }
    paint_rect(ctx) {
        const { p0, p1, p2, p3 } = this.rect();
        ctx.save();
        ctx.strokeStyle = "red";
        ctx.lineWidth = 1;
        ctx.beginPath();
        const { round } = Math;
        ctx.moveTo(round(p0.x), round(p0.y));
        ctx.lineTo(round(p1.x), round(p1.y));
        ctx.lineTo(round(p2.x), round(p2.y));
        ctx.lineTo(round(p3.x), round(p3.y));
        ctx.closePath();
        ctx.stroke();
        ctx.restore();
    }
    paint_bbox(ctx) {
        const { x, y, width, height } = this.bbox();
        ctx.save();
        ctx.strokeStyle = "blue";
        ctx.lineWidth = 1;
        ctx.beginPath();
        const { round } = Math;
        ctx.moveTo(round(x), round(y));
        ctx.lineTo(round(x), round(y + height));
        ctx.lineTo(round(x + width), round(y + height));
        ctx.lineTo(round(x + width), round(y));
        ctx.closePath();
        ctx.stroke();
        ctx.restore();
    }
}
GraphicsBox.__name__ = "GraphicsBox";
export class TextBox extends GraphicsBox {
    constructor({ text }) {
        super();
        //padding: Padding
        this._visual_align = "left";
        this.text = text;
    }
    set visuals(v) {
        const color = v.color;
        const alpha = v.alpha;
        const outline_color = v.outline_color;
        const style = v.font_style;
        let size = v.font_size;
        const face = v.font;
        const { font_size_scale, base_font_size } = this;
        const res = parse_css_font_size(size);
        if (res != null) {
            let { value, unit } = res;
            value *= font_size_scale;
            if (unit == "em" && base_font_size) {
                value *= base_font_size;
                unit = "px";
            }
            size = `${value}${unit}`;
        }
        const font = `${style} ${size} ${face}`;
        this.font = font;
        this.color = color2css(color, alpha);
        this.outline_color = color2css(outline_color, alpha);
        this.line_height = v.line_height;
        const align = v.align;
        this._visual_align = align;
        this._x_anchor = align;
        const baseline = v.baseline;
        this._y_anchor = (() => {
            switch (baseline) {
                case "top": return "top";
                case "middle": return "center";
                case "bottom": return "bottom";
                default: return "baseline";
            }
        })();
    }
    infer_text_height() {
        if (this.text.includes("\n"))
            return "ascent_descent";
        else {
            function is_math_like(text) {
                for (const c of new Set(text)) {
                    if ("0" <= c && c <= "9")
                        continue;
                    switch (c) {
                        case ",":
                        case ".":
                        case "+":
                        case "-":
                        case "\u2212":
                        case "e":
                            continue;
                        default:
                            return false;
                    }
                }
                return true;
            }
            if (is_math_like(this.text))
                return "cap";
            else
                return "ascent_descent";
        }
    }
    _text_line(fmetrics) {
        const metric = this.text_height_metric ?? this.infer_text_height();
        const ascent = (() => {
            switch (metric) {
                case "x":
                case "x_descent":
                    return fmetrics.x_height;
                case "cap":
                case "cap_descent":
                    return fmetrics.cap_height;
                case "ascent":
                case "ascent_descent":
                    return fmetrics.ascent;
            }
        })();
        const descent = (() => {
            switch (metric) {
                case "x":
                case "cap":
                case "ascent":
                    return 0;
                case "x_descent":
                case "cap_descent":
                case "ascent_descent":
                    return fmetrics.descent;
            }
        })();
        return { height: ascent + descent, ascent, descent };
    }
    get nlines() {
        const lines = this.text.split("\n");
        return lines.length;
    }
    _size() {
        const { font } = this;
        const fmetrics = font_metrics(font);
        const line_spacing = (this.line_height - 1) * fmetrics.height; // TODO: max(trailing(L[n-1]), leading(L[n]))
        const empty = this.text == "";
        const lines = this.text.split("\n");
        const nlines = lines.length;
        const widths = lines.map((line) => text_width(line, font));
        const text_line = this._text_line(fmetrics);
        const text_height = text_line.height * nlines;
        /*
        const heights: number[] = []
        const ascents: number[] = []
        const descents: number[] = []
    
        for (const line of lines) {
          const metrics = [...line].map((c) => glyph_metrics(c, font))
          const max_ascent = Math.max(max(metrics.map((m) => m.ascent)), fmetrics.cap_height)
          const max_descent = max(metrics.map((m) => m.descent))
          ascents.push(max_ascent)
          descents.push(max_descent)
          heights.push(max_ascent + max_descent)
        }
    
        const text_height = sum(heights)
        */
        const w_scale = this.width?.unit == "%" ? this.width.value : 1;
        const h_scale = this.height?.unit == "%" ? this.height.value : 1;
        const width = max(widths) * w_scale;
        const height = empty ? 0 : (text_height + line_spacing * (nlines - 1)) * h_scale;
        return { width, height, metrics: fmetrics };
    }
    _computed_position(size, metrics, nlines) {
        const { width, height } = size;
        const { sx, sy, x_anchor = this._x_anchor, y_anchor = this._y_anchor } = this.position;
        const x = sx - (() => {
            if (isNumber(x_anchor))
                return x_anchor * width;
            else {
                switch (x_anchor) {
                    case "left": return 0;
                    case "center": return 0.5 * width;
                    case "right": return width;
                }
            }
        })();
        const y = sy - (() => {
            if (isNumber(y_anchor))
                return y_anchor * height;
            else {
                switch (y_anchor) {
                    case "top": return 0;
                    case "center": return 0.5 * height;
                    case "bottom": return height;
                    case "baseline": {
                        if (nlines == 1) {
                            const metric = this.text_height_metric ?? this.infer_text_height();
                            switch (metric) {
                                case "x":
                                case "x_descent":
                                    return metrics.x_height;
                                case "cap":
                                case "cap_descent":
                                    return metrics.cap_height;
                                case "ascent":
                                case "ascent_descent":
                                    return metrics.ascent;
                            }
                        }
                        else
                            return 0.5 * height;
                    }
                }
            }
        })();
        return { x, y };
    }
    _rect() {
        const { width, height, metrics } = this._size();
        const nlines = this.text.split("\n").length;
        const { x, y } = this._computed_position({ width, height }, metrics, nlines);
        const bbox = new BBox({ x, y, width, height });
        return bbox.rect;
    }
    paint(ctx) {
        const { font } = this;
        const fmetrics = font_metrics(font);
        const line_spacing = (this.line_height - 1) * fmetrics.height; // TODO: see above
        const lines = this.text.split("\n");
        const nlines = lines.length;
        const widths = lines.map((line) => text_width(line, font));
        const text_line = this._text_line(fmetrics);
        const text_height = text_line.height * nlines;
        /*
        const heights: number[] = []
        const ascents: number[] = []
        const descents: number[] = []
    
        for (const line of lines) {
          const metrics = [...line].map((c) => glyph_metrics(c, font))
          const max_ascent = Math.max(max(metrics.map((m) => m.ascent)), fmetrics.cap_height)
          const max_descent = max(metrics.map((m) => m.descent))
          ascents.push(max_ascent)
          descents.push(max_descent)
          heights.push(max_ascent + max_descent)
        }
        */
        const w_scale = this.width?.unit == "%" ? this.width.value : 1;
        const h_scale = this.height?.unit == "%" ? this.height.value : 1;
        const width = max(widths) * w_scale;
        const height = (text_height + line_spacing * (nlines - 1)) * h_scale;
        ctx.save();
        ctx.fillStyle = this.color;
        ctx.strokeStyle = this.outline_color;
        ctx.font = this.font;
        ctx.textAlign = "left";
        ctx.textBaseline = "alphabetic";
        const { sx, sy } = this.position;
        const { align } = this;
        const { angle } = this;
        if (angle != null && angle != 0) {
            ctx.translate(sx, sy);
            ctx.rotate(angle);
            ctx.translate(-sx, -sy);
        }
        let { x, y } = this._computed_position({ width, height }, fmetrics, nlines);
        if (align == "justify") {
            for (let i = 0; i < nlines; i++) {
                let xij = x;
                const line = lines[i];
                const words = line.split(" ");
                const nwords = words.length;
                const word_widths = words.map((word) => text_width(word, font));
                const word_spacing = (width - sum(word_widths)) / (nwords - 1);
                for (let j = 0; j < nwords; j++) {
                    ctx.fillText(words[j], xij, y);
                    ctx.strokeText(words[j], xij, y);
                    xij += word_widths[j] + word_spacing;
                }
                y += /*heights[i]*/ text_line.height + line_spacing;
            }
        }
        else {
            for (let i = 0; i < nlines; i++) {
                const xi = x + (() => {
                    switch (align == "auto" ? this._visual_align : align) {
                        case "left": return 0;
                        case "center": return 0.5 * (width - widths[i]);
                        case "right": return width - widths[i];
                    }
                })();
                const linei = lines[i];
                const yi = y + /*ascents[i]*/ text_line.ascent;
                ctx.fillText(linei, xi, yi);
                ctx.strokeText(linei, xi, yi);
                y += /*heights[i]*/ text_line.height + line_spacing;
            }
        }
        ctx.restore();
    }
}
TextBox.__name__ = "TextBox";
export class BaseExpo extends GraphicsBox {
    constructor(base, expo) {
        super();
        this.base = base;
        this.expo = expo;
    }
    get children() {
        return [this.base, this.expo];
    }
    set base_font_size(v) {
        super.base_font_size = v;
        this.base.base_font_size = v;
        this.expo.base_font_size = v;
    }
    set position(p) {
        this._position = p;
        const bs = this.base.size();
        const es = this.expo.size();
        const shift = this._shift_scale() * bs.height;
        const height = Math.max(bs.height, shift + es.height);
        this.base.position = {
            sx: 0, x_anchor: "left",
            sy: height, y_anchor: "bottom",
        };
        this.expo.position = {
            sx: bs.width, x_anchor: "left",
            sy: shift, y_anchor: "bottom",
        };
    }
    get position() {
        return this._position;
    }
    set visuals(v) {
        this.expo.font_size_scale = 0.7;
        this.base.visuals = v;
        this.expo.visuals = v;
    }
    _shift_scale() {
        if (this.base instanceof TextBox && this.base.nlines == 1) {
            const { x_height, cap_height } = font_metrics(this.base.font);
            return x_height / cap_height;
        }
        else {
            return 2 / 3;
        }
    }
    infer_text_height() {
        return this.base.infer_text_height();
    }
    _rect() {
        const bb = this.base.bbox();
        const eb = this.expo.bbox();
        const bbox = bb.union(eb);
        const { x, y } = this._computed_position();
        return bbox.translate(x, y).rect;
    }
    _size() {
        const bs = this.base.size();
        const es = this.expo.size();
        return {
            width: bs.width + es.width,
            height: Math.max(bs.height, this._shift_scale() * bs.height + es.height),
        };
    }
    paint(ctx) {
        ctx.save();
        const { angle } = this;
        if (angle != null && angle != 0) {
            const { sx, sy } = this.position;
            ctx.translate(sx, sy);
            ctx.rotate(angle);
            ctx.translate(-sx, -sy);
        }
        const { x, y } = this._computed_position();
        ctx.translate(x, y);
        this.base.paint(ctx);
        this.expo.paint(ctx);
        ctx.restore();
    }
    // paint_rect ...
    paint_bbox(ctx) {
        super.paint_bbox(ctx);
        const { x, y } = this._computed_position();
        ctx.save();
        ctx.translate(x, y);
        for (const child of this.children) {
            child.paint_bbox(ctx);
        }
        ctx.restore();
    }
    _computed_position() {
        const { width, height } = this._size();
        const { sx, sy, x_anchor = this._x_anchor, y_anchor = this._y_anchor } = this.position;
        const x = sx - (() => {
            if (isNumber(x_anchor))
                return x_anchor * width;
            else {
                switch (x_anchor) {
                    case "left": return 0;
                    case "center": return 0.5 * width;
                    case "right": return width;
                }
            }
        })();
        const y = sy - (() => {
            if (isNumber(y_anchor))
                return y_anchor * height;
            else {
                switch (y_anchor) {
                    case "top": return 0;
                    case "center": return 0.5 * height;
                    case "bottom": return height;
                    case "baseline": return 0.5 * height; /* TODO */
                }
            }
        })();
        return { x, y };
    }
}
BaseExpo.__name__ = "BaseExpo";
export class GraphicsBoxes {
    constructor(items) {
        this.items = items;
    }
    set base_font_size(v) {
        for (const item of this.items) {
            item.base_font_size = v;
        }
    }
    get length() {
        return this.items.length;
    }
    set visuals(v) {
        for (const item of this.items) {
            item.visuals = v;
        }
        const metric_map = { x: 0, cap: 1, ascent: 2, x_descent: 3, cap_descent: 4, ascent_descent: 5 };
        const common = max_by(this.items.map((item) => item.infer_text_height()), (metric) => metric_map[metric]);
        for (const item of this.items) {
            item.text_height_metric = common;
        }
    }
    set angle(a) {
        for (const item of this.items) {
            item.angle = a;
        }
    }
    max_size() {
        let width = 0;
        let height = 0;
        for (const item of this.items) {
            const size = item.size();
            width = Math.max(width, size.width);
            height = Math.max(height, size.height);
        }
        return { width, height };
    }
}
GraphicsBoxes.__name__ = "GraphicsBoxes";
//# sourceMappingURL=graphics.js.map