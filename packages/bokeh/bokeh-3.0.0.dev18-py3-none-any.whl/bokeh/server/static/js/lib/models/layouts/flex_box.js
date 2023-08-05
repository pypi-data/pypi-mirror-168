var _a;
import { LayoutDOM, LayoutDOMView } from "./layout_dom";
import { GridAlignmentLayout } from "./alignments";
import { Container } from "../../core/layout/grid";
import { UIElement } from "../ui/ui_element";
import { px } from "../../core/dom";
export class FlexBoxView extends LayoutDOMView {
    connect_signals() {
        super.connect_signals();
        const { children } = this.model.properties;
        this.on_change(children, () => this.update_children());
    }
    get child_models() {
        return this.model.children;
    }
    _intrinsic_display() {
        return { inner: this.model.flow_mode, outer: "flex" };
    }
    _update_layout() {
        super._update_layout();
        this.style.append(":host", {
            flex_direction: this._direction,
            gap: px(this.model.spacing),
        });
        const layoutable = new Container();
        let r0 = 0;
        let c0 = 0;
        for (const view of this.child_views) {
            if (!(view instanceof LayoutDOMView))
                continue;
            const sizing = view.box_sizing();
            const flex = (() => {
                const policy = this._direction == "row" ? sizing.width_policy : sizing.height_policy;
                const size = this._direction == "row" ? sizing.width : sizing.height;
                const basis = size != null ? px(size) : "auto";
                switch (policy) {
                    case "auto":
                    case "fixed": return `0 0 ${basis}`;
                    case "fit": return "1 1 auto";
                    case "min": return "0 1 auto";
                    case "max": return "1 0 0px";
                }
            })();
            const align_self = (() => {
                const policy = this._direction == "row" ? sizing.height_policy : sizing.width_policy;
                switch (policy) {
                    case "auto":
                    case "fixed":
                    case "fit":
                    case "min": return this._direction == "row" ? sizing.valign : sizing.halign;
                    case "max": return "stretch";
                }
            })();
            view.style.append(":host", { flex, align_self });
            // undo `width/height: 100%` and let `align-self: strech` do the work
            if (this._direction == "row") {
                if (sizing.height_policy == "max")
                    view.style.append(":host", { height: "auto" });
            }
            else {
                if (sizing.width_policy == "max")
                    view.style.append(":host", { width: "auto" });
            }
            if (view.layout != null) {
                layoutable.add({ r0, c0, r1: r0 + 1, c1: c0 + 1 }, view);
                if (this._direction == "row")
                    c0 += 1;
                else
                    r0 += 1;
            }
        }
        if (layoutable.size != 0) {
            this.layout = new GridAlignmentLayout(layoutable);
            this.layout.set_sizing();
        }
        else {
            delete this.layout;
        }
    }
}
FlexBoxView.__name__ = "FlexBoxView";
export class FlexBox extends LayoutDOM {
    constructor(attrs) {
        super(attrs);
    }
}
_a = FlexBox;
FlexBox.__name__ = "FlexBox";
(() => {
    _a.define(({ Number, Array, Ref }) => ({
        children: [Array(Ref(UIElement)), []],
        spacing: [Number, 0],
    }));
})();
//# sourceMappingURL=flex_box.js.map