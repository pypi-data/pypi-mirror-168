var _a;
import { Signal0 } from "../../core/signaling";
import { Model } from "../../model";
import { Tool } from "./tool";
import { InspectTool } from "./inspectors/inspect_tool";
import { enumerate, flat_map, some } from "../../core/util/iterator";
export class ToolProxy extends Model {
    constructor(attrs) {
        super(attrs);
    }
    // Operates all the tools given only one button
    get underlying() {
        return this.tools[0];
    }
    get button_view() {
        return this.tools[0].button_view;
    }
    get event_type() {
        return this.tools[0].event_type;
    }
    get default_order() {
        return this.tools[0].default_order; // only gestures etc.
    }
    get tooltip() {
        return this.tools[0].tooltip;
    }
    get tool_name() {
        return this.tools[0].tool_name;
    }
    get computed_icon() {
        return this.tools[0].computed_icon;
    }
    get toggleable() {
        const tool = this.tools[0];
        return tool instanceof InspectTool && tool.toggleable;
    }
    get computed_overlays() {
        return [...flat_map(this.tools, (tool) => tool.computed_overlays)];
    }
    initialize() {
        super.initialize();
        this.do = new Signal0(this, "do");
    }
    connect_signals() {
        super.connect_signals();
        this.connect(this.do, () => this.doit());
        this.connect(this.properties.active.change, () => this.set_active());
        for (const tool of this.tools) {
            this.connect(tool.properties.active.change, () => {
                this.active = tool.active;
            });
        }
    }
    doit() {
        for (const tool of this.tools) {
            tool.do.emit();
        }
    }
    set_active() {
        for (const tool of this.tools) {
            tool.active = this.active;
        }
    }
    get menu() {
        const { menu } = this.tools[0];
        if (menu == null)
            return null;
        const items = [];
        for (const [item, i] of enumerate(menu)) {
            if (item == null)
                items.push(null);
            else {
                const handler = () => {
                    for (const tool of this.tools) {
                        tool.menu?.[i]?.handler?.();
                    }
                };
                items.push({ ...item, handler });
            }
        }
        return items;
    }
}
_a = ToolProxy;
ToolProxy.__name__ = "ToolProxy";
(() => {
    _a.define(({ Boolean, Array, Ref }) => ({
        tools: [Array(Ref(Tool)), []],
        active: [Boolean, (self) => some(self.tools, (tool) => tool.active)],
        disabled: [Boolean, false],
    }));
})();
//# sourceMappingURL=tool_proxy.js.map