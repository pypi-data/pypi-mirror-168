import { ScreenArray } from "../types";
import { equals } from "./eq";
const { min, max } = Math;
export function empty() {
    return {
        x0: Infinity,
        y0: Infinity,
        x1: -Infinity,
        y1: -Infinity,
    };
}
export function positive_x() {
    return {
        x0: Number.MIN_VALUE,
        y0: -Infinity,
        x1: Infinity,
        y1: Infinity,
    };
}
export function positive_y() {
    return {
        x0: -Infinity,
        y0: Number.MIN_VALUE,
        x1: Infinity,
        y1: Infinity,
    };
}
export function union(a, b) {
    return {
        x0: min(a.x0, b.x0),
        x1: max(a.x1, b.x1),
        y0: min(a.y0, b.y0),
        y1: max(a.y1, b.y1),
    };
}
export class BBox {
    constructor(box, correct = false) {
        if (box == null) {
            this.x0 = 0;
            this.y0 = 0;
            this.x1 = 0;
            this.y1 = 0;
        }
        else if ("x0" in box) {
            const { x0, y0, x1, y1 } = box;
            if (!(x0 <= x1 && y0 <= y1))
                throw new Error(`invalid bbox {x0: ${x0}, y0: ${y0}, x1: ${x1}, y1: ${y1}}`);
            this.x0 = x0;
            this.y0 = y0;
            this.x1 = x1;
            this.y1 = y1;
        }
        else if ("x" in box) {
            const { x, y, width, height } = box;
            if (!(width >= 0 && height >= 0))
                throw new Error(`invalid bbox {x: ${x}, y: ${y}, width: ${width}, height: ${height}}`);
            this.x0 = x;
            this.y0 = y;
            this.x1 = x + width;
            this.y1 = y + height;
        }
        else {
            let left, right;
            let top, bottom;
            if ("width" in box) {
                if ("left" in box) {
                    left = box.left;
                    right = left + box.width;
                }
                else if ("right" in box) {
                    right = box.right;
                    left = right - box.width;
                }
                else {
                    const w2 = box.width / 2;
                    left = box.hcenter - w2;
                    right = box.hcenter + w2;
                }
            }
            else {
                left = box.left;
                right = box.right;
            }
            if ("height" in box) {
                if ("top" in box) {
                    top = box.top;
                    bottom = top + box.height;
                }
                else if ("bottom" in box) {
                    bottom = box.bottom;
                    top = bottom - box.height;
                }
                else {
                    const h2 = box.height / 2;
                    top = box.vcenter - h2;
                    bottom = box.vcenter + h2;
                }
            }
            else {
                top = box.top;
                bottom = box.bottom;
            }
            if (left > right || top > bottom) {
                if (correct) {
                    if (left > right)
                        left = right;
                    if (top > bottom)
                        top = bottom;
                }
                else
                    throw new Error(`invalid bbox {left: ${left}, top: ${top}, right: ${right}, bottom: ${bottom}}`);
            }
            this.x0 = left;
            this.y0 = top;
            this.x1 = right;
            this.y1 = bottom;
        }
    }
    static from_lrtb({ left, right, top, bottom }) {
        return new BBox({
            x0: Math.min(left, right),
            y0: Math.min(top, bottom),
            x1: Math.max(left, right),
            y1: Math.max(top, bottom),
        });
    }
    clone() {
        return new BBox(this);
    }
    equals(that) {
        return this.x0 == that.x0 && this.y0 == that.y0 &&
            this.x1 == that.x1 && this.y1 == that.y1;
    }
    [equals](that, cmp) {
        return cmp.eq(this.x0, that.x0) && cmp.eq(this.y0, that.y0) &&
            cmp.eq(this.x1, that.x1) && cmp.eq(this.y1, that.y1);
    }
    toString() {
        return `BBox({left: ${this.left}, top: ${this.top}, width: ${this.width}, height: ${this.height}})`;
    }
    get is_empty() {
        const { x0, x1, y0, y1 } = this;
        return x0 == 0 && x1 == 0 && y0 == 0 && y1 == 0;
    }
    get left() { return this.x0; }
    get top() { return this.y0; }
    get right() { return this.x1; }
    get bottom() { return this.y1; }
    get p0() { return [this.x0, this.y0]; }
    get p1() { return [this.x1, this.y1]; }
    get x() { return this.x0; }
    get y() { return this.y0; }
    get width() { return this.x1 - this.x0; }
    get height() { return this.y1 - this.y0; }
    get size() { return { width: this.width, height: this.height }; }
    get rect() {
        const { x0, y0, x1, y1 } = this;
        return {
            p0: { x: x0, y: y0 },
            p1: { x: x1, y: y0 },
            p2: { x: x1, y: y1 },
            p3: { x: x0, y: y1 },
        };
    }
    get box() {
        const { x, y, width, height } = this;
        return { x, y, width, height };
    }
    get lrtb() {
        const { left, right, top, bottom } = this;
        return { left, right, top, bottom };
    }
    get h_range() { return { start: this.x0, end: this.x1 }; }
    get v_range() { return { start: this.y0, end: this.y1 }; }
    get ranges() { return [this.h_range, this.v_range]; }
    get aspect() { return this.width / this.height; }
    get hcenter() { return (this.left + this.right) / 2; }
    get vcenter() { return (this.top + this.bottom) / 2; }
    get area() { return this.width * this.height; }
    relative() {
        const { width, height } = this;
        return new BBox({ x: 0, y: 0, width, height });
    }
    translate(tx, ty) {
        const { x, y, width, height } = this;
        return new BBox({ x: tx + x, y: ty + y, width, height });
    }
    relativize(x, y) {
        return [x - this.x, y - this.y];
    }
    contains(x, y) {
        return this.x0 <= x && x <= this.x1 && this.y0 <= y && y <= this.y1;
    }
    clip(x, y) {
        if (x < this.x0)
            x = this.x0;
        else if (x > this.x1)
            x = this.x1;
        if (y < this.y0)
            y = this.y0;
        else if (y > this.y1)
            y = this.y1;
        return [x, y];
    }
    grow_by(size) {
        return new BBox({
            left: this.left - size,
            right: this.right + size,
            top: this.top - size,
            bottom: this.bottom + size,
        });
    }
    shrink_by(size) {
        return new BBox({
            left: this.left + size,
            right: this.right - size,
            top: this.top + size,
            bottom: this.bottom - size,
        }, true);
    }
    union(that) {
        return new BBox({
            x0: min(this.x0, that.x0),
            y0: min(this.y0, that.y0),
            x1: max(this.x1, that.x1),
            y1: max(this.y1, that.y1),
        });
    }
    intersection(that) {
        if (!this.intersects(that))
            return null;
        else {
            return new BBox({
                x0: max(this.x0, that.x0),
                y0: max(this.y0, that.y0),
                x1: min(this.x1, that.x1),
                y1: min(this.y1, that.y1),
            });
        }
    }
    intersects(that) {
        return !(that.x1 < this.x0 || that.x0 > this.x1 ||
            that.y1 < this.y0 || that.y0 > this.y1);
    }
    get xview() {
        return {
            compute: (x) => {
                return this.left + x;
            },
            v_compute: (xx) => {
                const _xx = new ScreenArray(xx.length);
                const left = this.left;
                for (let i = 0; i < xx.length; i++) {
                    _xx[i] = left + xx[i];
                }
                return _xx;
            },
        };
    }
    get yview() {
        return {
            compute: (y) => {
                return this.bottom - y;
            },
            v_compute: (yy) => {
                const _yy = new ScreenArray(yy.length);
                const bottom = this.bottom;
                for (let i = 0; i < yy.length; i++) {
                    _yy[i] = bottom - yy[i];
                }
                return _yy;
            },
        };
    }
}
BBox.__name__ = "BBox";
//# sourceMappingURL=bbox.js.map