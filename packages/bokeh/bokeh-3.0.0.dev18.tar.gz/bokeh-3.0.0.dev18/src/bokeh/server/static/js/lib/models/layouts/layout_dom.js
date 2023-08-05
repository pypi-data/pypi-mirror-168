var _a;
import { UIElement, UIElementView } from "../ui/ui_element";
import { Menu } from "../menus/menu";
import { Signal } from "../../core/signaling";
import { Align, Dimensions, FlowMode, SizingMode } from "../../core/enums";
import { remove, px } from "../../core/dom";
import { isNumber, isArray } from "../../core/util/types";
import { build_views } from "../../core/build_views";
import { SizingPolicy } from "../../core/layout";
import { defer } from "../../core/util/defer";
import { CanvasLayer } from "../../core/util/canvas";
import { unreachable } from "../../core/util/assert";
export class LayoutDOMView extends UIElementView {
    constructor() {
        super(...arguments);
        this.mouseenter = new Signal(this, "mouseenter");
        this.mouseleave = new Signal(this, "mouseleave");
        this.disabled = new Signal(this, "disabled");
        this._resized = false;
        this._auto_width = "fit-content";
        this._auto_height = "fit-content";
    }
    get is_layout_root() {
        return this.is_root || !(this.parent instanceof LayoutDOMView);
    }
    initialize() {
        super.initialize();
        this._child_views = new Map();
    }
    _after_resize() {
        this._resized = true;
        super._after_resize();
        this.compute_layout();
    }
    async lazy_initialize() {
        await super.lazy_initialize();
        await this.build_child_views();
    }
    remove() {
        for (const child_view of this.child_views)
            child_view.remove();
        this._child_views.clear();
        super.remove();
    }
    connect_signals() {
        super.connect_signals();
        this.el.addEventListener("mouseenter", (event) => {
            this.mouseenter.emit(event);
        });
        this.el.addEventListener("mouseleave", (event) => {
            this.mouseleave.emit(event);
        });
        this.el.addEventListener("contextmenu", (event) => {
            if (this.model.context_menu != null) {
                console.log("context menu");
                event.preventDefault();
            }
        });
        if (this.parent instanceof LayoutDOMView) {
            this.connect(this.parent.disabled, (disabled) => {
                this.disabled.emit(disabled || this.model.disabled);
            });
        }
        const p = this.model.properties;
        this.on_change(p.disabled, () => {
            this.disabled.emit(this.model.disabled);
        });
        this.on_change([
            p.width, p.height,
            p.min_width, p.min_height,
            p.max_width, p.max_height,
            p.margin,
            p.width_policy, p.height_policy,
            p.flow_mode, p.sizing_mode,
            p.aspect_ratio,
            p.visible,
        ], () => this.invalidate_layout());
        this.on_change([
            p.css_classes,
            p.stylesheets,
        ], () => this.invalidate_render());
    }
    css_classes() {
        return [...super.css_classes(), ...this.model.css_classes];
    }
    *children() {
        yield* super.children();
        yield* this.child_views;
    }
    get child_views() {
        return this.child_models.map((child) => this._child_views.get(child));
    }
    async build_child_views() {
        const { created, removed } = await build_views(this._child_views, this.child_models, { parent: this });
        for (const view of removed) {
            this._resize_observer.unobserve(view.el);
        }
        for (const view of created) {
            this._resize_observer.observe(view.el, { box: "border-box" });
        }
        return created;
    }
    render() {
        super.render();
        this.class_list.add(...this.css_classes());
        for (const child_view of this.child_views) {
            this.shadow_el.appendChild(child_view.el);
            child_view.render();
            child_view.after_render();
        }
    }
    _update_children() { }
    async update_children() {
        const created_children = new Set(await this.build_child_views());
        for (const child_view of this.child_views) {
            remove(child_view.el);
        }
        for (const child_view of this.child_views) {
            this.shadow_el.appendChild(child_view.el);
            if (created_children.has(child_view)) {
                child_view.render();
                child_view.after_render();
            }
        }
        this._update_children();
        this.invalidate_layout();
    }
    _intrinsic_display() {
        return { inner: this.model.flow_mode, outer: "flow" };
    }
    _update_layout() {
        function css_sizing(policy, size, auto_size) {
            switch (policy) {
                case "auto":
                    return size != null ? px(size) : auto_size;
                case "fixed":
                    return size != null ? px(size) : "fit-content";
                case "fit":
                    return "fit-content";
                case "min":
                    return "min-content";
                case "max":
                    return "100%";
            }
        }
        function css_display(display) {
            // Convert to legacy values due to limitted browser support.
            const { inner, outer } = display;
            switch (`${inner} ${outer}`) {
                case "block flow": return "block";
                case "inline flow": return "inline";
                case "block flow-root": return "flow-root";
                case "inline flow-root": return "inline-block";
                case "block flex": return "flex";
                case "inline flex": return "inline-flex";
                case "block grid": return "grid";
                case "inline grid": return "inline-grid";
                case "block table": return "table";
                case "inline table": return "inline-table";
                default: unreachable();
            }
        }
        function to_css(value) {
            return isNumber(value) ? px(value) : `${value.percent}%`;
        }
        const styles = {};
        const display = this._intrinsic_display();
        styles.display = css_display(display);
        const sizing = this.box_sizing();
        const { width_policy, height_policy, width, height, aspect_ratio } = sizing;
        const computed_aspect = (() => {
            if (aspect_ratio == "auto") {
                if (width != null && height != null)
                    return width / height;
            }
            else if (isNumber(aspect_ratio))
                return aspect_ratio;
            return null;
        })();
        if (aspect_ratio == "auto") {
            if (width != null && height != null)
                styles.aspect_ratio = `${width} / ${height}`;
            else
                styles.aspect_ratio = "auto";
        }
        else if (isNumber(aspect_ratio))
            styles.aspect_ratio = `${aspect_ratio}`;
        const [css_width, css_height] = (() => {
            const css_width = css_sizing(width_policy, width, this._auto_width);
            const css_height = css_sizing(height_policy, height, this._auto_height);
            if (aspect_ratio != null) {
                if (width_policy != height_policy) {
                    if (width_policy == "fixed")
                        return [css_width, "auto"];
                    if (height_policy == "fixed")
                        return ["auto", css_height];
                    if (width_policy == "max")
                        return [css_width, "auto"];
                    if (height_policy == "max")
                        return ["auto", css_height];
                    return ["auto", "auto"];
                }
                else {
                    if (width_policy != "fixed" && height_policy != "fixed") {
                        if (computed_aspect != null) {
                            if (computed_aspect >= 1)
                                return [css_width, "auto"];
                            else
                                return ["auto", css_height];
                        }
                    }
                }
            }
            return [css_width, css_height];
        })();
        styles.width = css_width;
        styles.height = css_height;
        const { min_width, max_width } = this.model;
        const { min_height, max_height } = this.model;
        styles.min_width = min_width == null ? "0px" : to_css(min_width);
        styles.min_height = min_height == null ? "0px" : to_css(min_height);
        if (this.is_layout_root) {
            if (max_width != null)
                styles.max_width = to_css(max_width);
            if (max_height != null)
                styles.max_height = to_css(max_height);
        }
        else {
            if (max_width != null)
                styles.max_width = `min(${to_css(max_width)}, 100%)`;
            else if (width_policy != "fixed")
                styles.max_width = "100%";
            if (max_height != null)
                styles.max_height = `min(${to_css(max_height)}, 100%)`;
            else if (height_policy != "fixed")
                styles.max_height = "100%";
        }
        const { margin } = this.model;
        if (margin != null) {
            if (isNumber(margin))
                styles.margin = px(margin);
            else if (margin.length == 2) {
                const [vertical, horizontal] = margin;
                styles.margin = `${px(vertical)} ${px(horizontal)}`;
            }
            else {
                const [top, right, bottom, left] = margin;
                styles.margin = `${px(top)} ${px(right)} ${px(bottom)} ${px(left)}`;
            }
        }
        const { resizable } = this.model;
        if (resizable !== false) {
            const resize = (() => {
                switch (resizable) {
                    case "width": return "horizontal";
                    case "height": return "vertical";
                    case true:
                    case "both": return "both";
                }
            })();
            styles.resize = resize;
            styles.overflow = "auto";
        }
        this.style.append(":host", styles);
    }
    update_layout() {
        this.update_style();
        for (const child_view of this.child_views) {
            if (child_view instanceof LayoutDOMView)
                child_view.update_layout();
        }
        this._update_layout();
    }
    get is_managed() {
        return this.parent instanceof LayoutDOMView;
    }
    /**
     * Update CSS layout with computed values from canvas layout.
     * This can be done more frequently than `_update_layout()`.
     */
    _measure_layout() { }
    measure_layout() {
        for (const child_view of this.child_views) {
            if (child_view instanceof LayoutDOMView)
                child_view.measure_layout();
        }
        this._measure_layout();
    }
    compute_layout() {
        if (this.parent instanceof LayoutDOMView) {
            //if (this.is_managed) {
            this.parent.compute_layout();
        }
        else {
            this.measure_layout();
            this.update_bbox();
            if (this.layout != null)
                this.layout.compute(this.bbox.size);
            else {
                for (const child_view of this.child_views) {
                    if (child_view instanceof LayoutDOMView && child_view.layout != null)
                        child_view.layout.compute(child_view.bbox.size);
                }
            }
            this.after_layout();
        }
    }
    update_bbox() {
        for (const child_view of this.child_views) {
            child_view.update_bbox();
        }
        super.update_bbox();
    }
    _after_layout() { }
    after_layout() {
        for (const child_view of this.child_views) {
            if (child_view instanceof LayoutDOMView)
                child_view.after_layout();
        }
        this._after_layout();
    }
    render_to(element) {
        element.appendChild(this.el);
        this.build();
        this.notify_finished();
    }
    after_render() {
        if (!this.is_managed) {
            this.invalidate_layout();
        }
        if (!this._has_finished) {
            if (!this._is_displayed) {
                this.finish();
            }
            else {
                // In case after_resize() wasn't called (see regression test for issue
                // #9113), then wait one macro task and consider this view finished.
                defer().then(() => {
                    if (!this._resized) {
                        this.finish();
                    }
                });
            }
        }
    }
    build() {
        if (!this.is_layout_root)
            throw new Error(`${this.toString()} is not a root layout`);
        this.render();
        this.after_render();
        return this;
    }
    async rebuild() {
        await this.build_child_views();
        this.invalidate_render();
    }
    invalidate_layout() {
        // TODO: it would be better and more efficient to do a localized
        // update, but for now this guarantees consistent state of layout.
        if (this.parent instanceof LayoutDOMView) {
            this.parent.invalidate_layout();
        }
        else {
            this.update_layout();
            this.compute_layout();
        }
    }
    invalidate_render() {
        this.render();
        this.invalidate_layout();
    }
    has_finished() {
        if (!super.has_finished())
            return false;
        for (const child_view of this.child_views) {
            if (!child_view.has_finished())
                return false;
        }
        return true;
    }
    box_sizing() {
        let { width_policy, height_policy, aspect_ratio } = this.model;
        const { sizing_mode } = this.model;
        if (sizing_mode != null) {
            if (sizing_mode == "fixed")
                width_policy = height_policy = "fixed";
            else if (sizing_mode == "stretch_both")
                width_policy = height_policy = "max";
            else if (sizing_mode == "stretch_width")
                width_policy = "max";
            else if (sizing_mode == "stretch_height")
                height_policy = "max";
            else {
                if (aspect_ratio == null)
                    aspect_ratio = "auto";
                switch (sizing_mode) {
                    case "scale_width":
                        width_policy = "max";
                        height_policy = "min";
                        break;
                    case "scale_height":
                        width_policy = "min";
                        height_policy = "max";
                        break;
                    case "scale_both":
                        width_policy = "max";
                        height_policy = "max";
                        break;
                }
            }
        }
        const [halign, valign] = (() => {
            const { align } = this.model;
            if (align == "auto")
                return [undefined, undefined];
            else if (isArray(align))
                return align;
            else
                return [align, align];
        })();
        const { width, height } = this.model;
        return {
            width_policy,
            height_policy,
            width,
            height,
            aspect_ratio,
            halign,
            valign,
        };
    }
    export(type = "auto", hidpi = true) {
        const output_backend = (() => {
            switch (type) {
                case "auto": // TODO: actually infer the best type
                case "png": return "canvas";
                case "svg": return "svg";
            }
        })();
        const composite = new CanvasLayer(output_backend, hidpi);
        const { x, y, width, height } = this.bbox;
        composite.resize(width, height);
        const bg_color = getComputedStyle(this.el).backgroundColor;
        composite.ctx.fillStyle = bg_color;
        composite.ctx.fillRect(x, y, width, height);
        for (const view of this.child_views) {
            const region = view.export(type, hidpi);
            const { x, y } = view.bbox;
            composite.ctx.drawImage(region.canvas, x, y);
        }
        return composite;
    }
    serializable_state() {
        return {
            ...super.serializable_state(),
            children: this.child_views.map((child) => child.serializable_state()),
        };
    }
}
LayoutDOMView.__name__ = "LayoutDOMView";
export class LayoutDOM extends UIElement {
    constructor(attrs) {
        super(attrs);
    }
}
_a = LayoutDOM;
LayoutDOM.__name__ = "LayoutDOM";
(() => {
    _a.define((types) => {
        const { Boolean, Number, String, Auto, Array, Tuple, Or, Null, Nullable, Ref } = types;
        const Number2 = Tuple(Number, Number);
        const Number4 = Tuple(Number, Number, Number, Number);
        return {
            width: [Nullable(Number), null],
            height: [Nullable(Number), null],
            min_width: [Nullable(Number), null],
            min_height: [Nullable(Number), null],
            max_width: [Nullable(Number), null],
            max_height: [Nullable(Number), null],
            margin: [Nullable(Or(Number, Number2, Number4)), null],
            width_policy: [Or(SizingPolicy, Auto), "auto"],
            height_policy: [Or(SizingPolicy, Auto), "auto"],
            aspect_ratio: [Or(Number, Auto, Null), null],
            flow_mode: [FlowMode, "block"],
            sizing_mode: [Nullable(SizingMode), null],
            disabled: [Boolean, false],
            align: [Or(Align, Tuple(Align, Align), Auto), "auto"],
            css_classes: [Array(String), []],
            context_menu: [Nullable(Ref(Menu)), null],
            resizable: [Or(Boolean, Dimensions), false],
        };
    });
})();
//# sourceMappingURL=layout_dom.js.map