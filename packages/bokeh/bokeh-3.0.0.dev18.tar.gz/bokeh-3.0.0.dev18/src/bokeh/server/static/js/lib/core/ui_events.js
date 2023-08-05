import Hammer from "hammerjs";
import { Signal } from "./signaling";
import { logger } from "./logging";
import { offset_bbox } from "./dom";
import * as events from "./bokeh_events";
import { getDeltaY } from "./util/wheel";
import { reversed, is_empty } from "./util/array";
import { isString } from "./util/types";
import { is_mobile } from "./util/platform";
function is_touch(event) {
    return typeof TouchEvent !== "undefined" && event instanceof TouchEvent;
}
export class UIEventBus {
    constructor(canvas_view) {
        this.canvas_view = canvas_view;
        this.pan_start = new Signal(this, "pan:start");
        this.pan = new Signal(this, "pan");
        this.pan_end = new Signal(this, "pan:end");
        this.pinch_start = new Signal(this, "pinch:start");
        this.pinch = new Signal(this, "pinch");
        this.pinch_end = new Signal(this, "pinch:end");
        this.rotate_start = new Signal(this, "rotate:start");
        this.rotate = new Signal(this, "rotate");
        this.rotate_end = new Signal(this, "rotate:end");
        this.tap = new Signal(this, "tap");
        this.doubletap = new Signal(this, "doubletap");
        this.press = new Signal(this, "press");
        this.pressup = new Signal(this, "pressup");
        this.move_enter = new Signal(this, "move:enter");
        this.move = new Signal(this, "move");
        this.move_exit = new Signal(this, "move:exit");
        this.scroll = new Signal(this, "scroll");
        this.keydown = new Signal(this, "keydown");
        this.keyup = new Signal(this, "keyup");
        this.hammer = new Hammer(this.hit_area, {
            cssProps: {},
            touchAction: "auto",
            inputClass: Hammer.TouchMouseInput, // https://github.com/bokeh/bokeh/issues/9187
        });
        this._prev_move = null;
        this._curr_pan = null;
        this._curr_pinch = null;
        this._curr_rotate = null;
        this._configure_hammerjs();
        // Mouse & keyboard events not handled through hammerjs
        // We can 'add and forget' these event listeners because this.hit_area is a DOM element
        // that will be thrown away when the view is removed
        this.hit_area.addEventListener("mousemove", (e) => this._mouse_move(e));
        this.hit_area.addEventListener("mouseenter", (e) => this._mouse_enter(e));
        this.hit_area.addEventListener("mouseleave", (e) => this._mouse_exit(e));
        this.hit_area.addEventListener("contextmenu", (e) => this._context_menu(e));
        this.hit_area.addEventListener("wheel", (e) => this._mouse_wheel(e));
        // But we MUST remove listeners registered on document or we'll leak memory: register
        // 'this' as the listener (it implements the event listener interface, i.e. handleEvent)
        // instead of an anonymous function so we can easily refer back to it for removing
        document.addEventListener("keydown", this);
        document.addEventListener("keyup", this);
    }
    get hit_area() {
        return this.canvas_view.events_el;
    }
    destroy() {
        this.hammer.destroy();
        document.removeEventListener("keydown", this);
        document.removeEventListener("keyup", this);
    }
    handleEvent(e) {
        if (e.type == "keydown")
            this._key_down(e);
        else if (e.type == "keyup")
            this._key_up(e);
    }
    _configure_hammerjs() {
        // This is to be able to distinguish double taps from single taps
        this.hammer.get("doubletap").recognizeWith("tap");
        this.hammer.get("tap").requireFailure("doubletap");
        this.hammer.get("doubletap").dropRequireFailure("tap");
        this.hammer.on("doubletap", (e) => this._doubletap(e));
        this.hammer.on("tap", (e) => this._tap(e));
        this.hammer.on("press", (e) => this._press(e));
        this.hammer.on("pressup", (e) => this._pressup(e));
        this.hammer.get("pan").set({ direction: Hammer.DIRECTION_ALL });
        this.hammer.on("panstart", (e) => this._pan_start(e));
        this.hammer.on("pan", (e) => this._pan(e));
        this.hammer.on("panend", (e) => this._pan_end(e));
        this.hammer.get("pinch").set({ enable: true });
        this.hammer.on("pinchstart", (e) => this._pinch_start(e));
        this.hammer.on("pinch", (e) => this._pinch(e));
        this.hammer.on("pinchend", (e) => this._pinch_end(e));
        this.hammer.get("rotate").set({ enable: true });
        this.hammer.on("rotatestart", (e) => this._rotate_start(e));
        this.hammer.on("rotate", (e) => this._rotate(e));
        this.hammer.on("rotateend", (e) => this._rotate_end(e));
    }
    register_tool(tool_view) {
        const et = tool_view.model.event_type;
        if (et != null) {
            if (isString(et))
                this._register_tool(tool_view, et);
            else {
                // Multi-tools should only registered shared events once
                et.forEach((e, index) => this._register_tool(tool_view, e, index < 1));
            }
        }
    }
    _register_tool(tool_view, et, shared = true) {
        const v = tool_view;
        const { id } = v.model;
        const conditionally = (fn) => (arg) => {
            if (arg.id == id)
                fn(arg.e);
        };
        const unconditionally = (fn) => (arg) => {
            fn(arg.e);
        };
        switch (et) {
            case "pan": {
                if (v._pan_start != null)
                    v.connect(this.pan_start, conditionally(v._pan_start.bind(v)));
                if (v._pan != null)
                    v.connect(this.pan, conditionally(v._pan.bind(v)));
                if (v._pan_end != null)
                    v.connect(this.pan_end, conditionally(v._pan_end.bind(v)));
                break;
            }
            case "pinch": {
                if (v._pinch_start != null)
                    v.connect(this.pinch_start, conditionally(v._pinch_start.bind(v)));
                if (v._pinch != null)
                    v.connect(this.pinch, conditionally(v._pinch.bind(v)));
                if (v._pinch_end != null)
                    v.connect(this.pinch_end, conditionally(v._pinch_end.bind(v)));
                break;
            }
            case "rotate": {
                if (v._rotate_start != null)
                    v.connect(this.rotate_start, conditionally(v._rotate_start.bind(v)));
                if (v._rotate != null)
                    v.connect(this.rotate, conditionally(v._rotate.bind(v)));
                if (v._rotate_end != null)
                    v.connect(this.rotate_end, conditionally(v._rotate_end.bind(v)));
                break;
            }
            case "move": {
                if (v._move_enter != null)
                    v.connect(this.move_enter, conditionally(v._move_enter.bind(v)));
                if (v._move != null)
                    v.connect(this.move, conditionally(v._move.bind(v)));
                if (v._move_exit != null)
                    v.connect(this.move_exit, conditionally(v._move_exit.bind(v)));
                break;
            }
            case "tap": {
                if (v._tap != null)
                    v.connect(this.tap, conditionally(v._tap.bind(v)));
                if (v._doubletap != null)
                    v.connect(this.doubletap, conditionally(v._doubletap.bind(v)));
                break;
            }
            case "press": {
                if (v._press != null)
                    v.connect(this.press, conditionally(v._press.bind(v)));
                if (v._pressup != null)
                    v.connect(this.pressup, conditionally(v._pressup.bind(v)));
                break;
            }
            case "scroll": {
                if (v._scroll != null)
                    v.connect(this.scroll, conditionally(v._scroll.bind(v)));
                break;
            }
            default:
                throw new Error(`unsupported event_type: ${et}`);
        }
        // Skip shared events if registering multi-tool
        if (!shared)
            return;
        if (v._keydown != null)
            v.connect(this.keydown, unconditionally(v._keydown.bind(v)));
        if (v._keyup != null)
            v.connect(this.keyup, unconditionally(v._keyup.bind(v)));
        // Dual touch hack part 1/2
        // This is a hack for laptops with touch screen who may be pinching or scrolling
        // in order to use the wheel zoom tool. If it's a touch screen the WheelZoomTool event
        // will be linked to pinch. But we also want to trigger in the case of a scroll.
        if (is_mobile && v._scroll != null && et == "pinch") {
            logger.debug("Registering scroll on touch screen");
            v.connect(this.scroll, conditionally(v._scroll.bind(v)));
        }
    }
    _hit_test_renderers(plot_view, sx, sy) {
        const views = plot_view.get_renderer_views();
        for (const view of reversed(views)) {
            if (view.interactive_hit?.(sx, sy) ?? false)
                return view;
        }
        return null;
    }
    set_cursor(cursor = "default") {
        this.hit_area.style.cursor = cursor;
    }
    _hit_test_frame(plot_view, sx, sy) {
        return plot_view.frame.bbox.contains(sx, sy);
    }
    _hit_test_plot(sx, sy) {
        // TODO: z-index
        for (const plot_view of this.canvas_view.plot_views) {
            if (plot_view.bbox.relative() /*XXX*/.contains(sx, sy))
                return plot_view;
        }
        return null;
    }
    _trigger(signal, e, srcEvent) {
        const { sx, sy } = e;
        const plot_view = this._hit_test_plot(sx, sy);
        const curr_view = plot_view;
        const relativize_event = (_plot_view) => {
            const [rel_sx, rel_sy] = [sx, sy]; // plot_view.layout.bbox.relativize(sx, sy)
            return { ...e, sx: rel_sx, sy: rel_sy };
        };
        if (e.type == "panstart" || e.type == "pan" || e.type == "panend") {
            let pan_view;
            if (e.type == "panstart" && curr_view != null) {
                this._curr_pan = { plot_view: curr_view };
                pan_view = curr_view;
            }
            else if (e.type == "pan" && this._curr_pan != null) {
                pan_view = this._curr_pan.plot_view;
            }
            else if (e.type == "panend" && this._curr_pan != null) {
                pan_view = this._curr_pan.plot_view;
                this._curr_pan = null;
            }
            else {
                pan_view = null;
            }
            if (pan_view != null) {
                const event = relativize_event(pan_view);
                this.__trigger(pan_view, signal, event, srcEvent);
            }
        }
        else if (e.type == "pinchstart" || e.type == "pinch" || e.type == "pinchend") {
            let pinch_view;
            if (e.type == "pinchstart" && curr_view != null) {
                this._curr_pinch = { plot_view: curr_view };
                pinch_view = curr_view;
            }
            else if (e.type == "pinch" && this._curr_pinch != null) {
                pinch_view = this._curr_pinch.plot_view;
            }
            else if (e.type == "pinchend" && this._curr_pinch != null) {
                pinch_view = this._curr_pinch.plot_view;
                this._curr_pinch = null;
            }
            else {
                pinch_view = null;
            }
            if (pinch_view != null) {
                const event = relativize_event(pinch_view);
                this.__trigger(pinch_view, signal, event, srcEvent);
            }
        }
        else if (e.type == "rotatestart" || e.type == "rotate" || e.type == "rotateend") {
            let rotate_view;
            if (e.type == "rotatestart" && curr_view != null) {
                this._curr_rotate = { plot_view: curr_view };
                rotate_view = curr_view;
            }
            else if (e.type == "rotate" && this._curr_rotate != null) {
                rotate_view = this._curr_rotate.plot_view;
            }
            else if (e.type == "rotateend" && this._curr_rotate != null) {
                rotate_view = this._curr_rotate.plot_view;
                this._curr_rotate = null;
            }
            else {
                rotate_view = null;
            }
            if (rotate_view != null) {
                const event = relativize_event(rotate_view);
                this.__trigger(rotate_view, signal, event, srcEvent);
            }
        }
        else if (e.type == "mouseenter" || e.type == "mousemove" || e.type == "mouseleave") {
            const prev_view = this._prev_move?.plot_view;
            if (prev_view != null && (e.type == "mouseleave" || prev_view != curr_view)) {
                const { sx, sy } = relativize_event(prev_view);
                this.__trigger(prev_view, this.move_exit, { type: "mouseleave", sx, sy, shiftKey: false, ctrlKey: false }, srcEvent);
            }
            if (curr_view != null && (e.type == "mouseenter" || prev_view != curr_view)) {
                const { sx, sy } = relativize_event(curr_view);
                this.__trigger(curr_view, this.move_enter, { type: "mouseenter", sx, sy, shiftKey: false, ctrlKey: false }, srcEvent);
            }
            if (curr_view != null && e.type == "mousemove") {
                const event = relativize_event(curr_view);
                this.__trigger(curr_view, signal, event, srcEvent);
            }
            this._prev_move = { sx, sy, plot_view: curr_view };
        }
        else {
            if (curr_view != null) {
                const event = relativize_event(curr_view);
                this.__trigger(curr_view, signal, event, srcEvent);
            }
        }
    }
    __trigger(plot_view, signal, e, srcEvent) {
        const gestures = plot_view.model.toolbar.gestures;
        const event_type = signal.name;
        const base_type = event_type.split(":")[0];
        const view = this._hit_test_renderers(plot_view, e.sx, e.sy);
        switch (base_type) {
            case "move": {
                const active_gesture = gestures.move.active;
                if (active_gesture != null)
                    this.trigger(signal, e, active_gesture.id);
                const active_inspectors = plot_view.model.toolbar.inspectors.filter(t => t.active);
                let cursor = "default";
                // the event happened on a renderer
                if (view != null) {
                    cursor = view.cursor(e.sx, e.sy) ?? cursor;
                    if (!is_empty(active_inspectors)) {
                        // override event_type to cause inspectors to clear overlays
                        signal = this.move_exit; // XXX
                    }
                    // the event happened on the plot frame but off a renderer
                }
                else if (this._hit_test_frame(plot_view, e.sx, e.sy)) {
                    if (!is_empty(active_inspectors)) {
                        cursor = "crosshair";
                    }
                }
                this.set_cursor(cursor);
                active_inspectors.map((inspector) => this.trigger(signal, e, inspector.id));
                break;
            }
            case "tap": {
                // XXX: hammerjs, why non-standard path?
                const path = srcEvent.path ?? srcEvent.composedPath();
                if (path.length != 0 && path[0] != this.hit_area)
                    return; // don't trigger bokeh events
                view?.on_hit?.(e.sx, e.sy);
                if (this._hit_test_frame(plot_view, e.sx, e.sy)) {
                    const active_gesture = gestures.tap.active;
                    if (active_gesture != null)
                        this.trigger(signal, e, active_gesture.id);
                }
                break;
            }
            case "doubletap": {
                if (this._hit_test_frame(plot_view, e.sx, e.sy)) {
                    const active_gesture = gestures.doubletap.active ?? gestures.tap.active;
                    if (active_gesture != null)
                        this.trigger(signal, e, active_gesture.id);
                }
                break;
            }
            case "scroll": {
                // Dual touch hack part 2/2
                // This is a hack for laptops with touch screen who may be pinching or scrolling
                // in order to use the wheel zoom tool. If it's a touch screen the WheelZoomTool event
                // will be linked to pinch. But we also want to trigger in the case of a scroll.
                const base = is_mobile ? "pinch" : "scroll";
                const active_gesture = gestures[base].active;
                if (active_gesture != null) {
                    srcEvent.preventDefault();
                    srcEvent.stopPropagation();
                    this.trigger(signal, e, active_gesture.id);
                }
                break;
            }
            case "pan": {
                const active_gesture = gestures.pan.active;
                if (active_gesture != null) {
                    srcEvent.preventDefault();
                    this.trigger(signal, e, active_gesture.id);
                }
                break;
            }
            default: {
                const active_gesture = gestures[base_type].active;
                if (active_gesture != null)
                    this.trigger(signal, e, active_gesture.id);
            }
        }
        this._trigger_bokeh_event(plot_view, e);
    }
    trigger(signal, e, id = null) {
        signal.emit({ id, e });
    }
    /*protected*/ _trigger_bokeh_event(plot_view, e) {
        const ev = (() => {
            const { sx, sy } = e;
            const x = plot_view.frame.x_scale.invert(sx);
            const y = plot_view.frame.y_scale.invert(sy);
            switch (e.type) {
                case "wheel":
                    return new events.MouseWheel(sx, sy, x, y, e.delta);
                case "mousemove":
                    return new events.MouseMove(sx, sy, x, y);
                case "mouseenter":
                    return new events.MouseEnter(sx, sy, x, y);
                case "mouseleave":
                    return new events.MouseLeave(sx, sy, x, y);
                case "tap":
                    return new events.Tap(sx, sy, x, y);
                case "doubletap":
                    return new events.DoubleTap(sx, sy, x, y);
                case "press":
                    return new events.Press(sx, sy, x, y);
                case "pressup":
                    return new events.PressUp(sx, sy, x, y);
                case "pan":
                    return new events.Pan(sx, sy, x, y, e.deltaX, e.deltaY);
                case "panstart":
                    return new events.PanStart(sx, sy, x, y);
                case "panend":
                    return new events.PanEnd(sx, sy, x, y);
                case "pinch":
                    return new events.Pinch(sx, sy, x, y, e.scale);
                case "pinchstart":
                    return new events.PinchStart(sx, sy, x, y);
                case "pinchend":
                    return new events.PinchEnd(sx, sy, x, y);
                case "rotate":
                    return new events.Rotate(sx, sy, x, y, e.rotation);
                case "rotatestart":
                    return new events.RotateStart(sx, sy, x, y);
                case "rotateend":
                    return new events.RotateEnd(sx, sy, x, y);
                default:
                    return undefined;
            }
        })();
        if (ev != null)
            plot_view.model.trigger_event(ev);
    }
    /*private*/ _get_sxy(event) {
        const { pageX, pageY } = is_touch(event) ? (event.touches.length != 0 ? event.touches : event.changedTouches)[0] : event;
        const { left, top } = offset_bbox(this.hit_area);
        return {
            sx: pageX - left,
            sy: pageY - top,
        };
    }
    /*private*/ _pan_event(e) {
        return {
            type: e.type,
            ...this._get_sxy(e.srcEvent),
            deltaX: e.deltaX,
            deltaY: e.deltaY,
            shiftKey: e.srcEvent.shiftKey,
            ctrlKey: e.srcEvent.ctrlKey,
        };
    }
    /*private*/ _pinch_event(e) {
        return {
            type: e.type,
            ...this._get_sxy(e.srcEvent),
            scale: e.scale,
            shiftKey: e.srcEvent.shiftKey,
            ctrlKey: e.srcEvent.ctrlKey,
        };
    }
    /*private*/ _rotate_event(e) {
        return {
            type: e.type,
            ...this._get_sxy(e.srcEvent),
            rotation: e.rotation,
            shiftKey: e.srcEvent.shiftKey,
            ctrlKey: e.srcEvent.ctrlKey,
        };
    }
    /*private*/ _tap_event(e) {
        return {
            type: e.type,
            ...this._get_sxy(e.srcEvent),
            shiftKey: e.srcEvent.shiftKey,
            ctrlKey: e.srcEvent.ctrlKey,
        };
    }
    /*private*/ _move_event(e) {
        return {
            type: e.type,
            ...this._get_sxy(e),
            shiftKey: e.shiftKey,
            ctrlKey: e.ctrlKey,
        };
    }
    /*private*/ _scroll_event(e) {
        return {
            type: e.type,
            ...this._get_sxy(e),
            delta: getDeltaY(e),
            shiftKey: e.shiftKey,
            ctrlKey: e.ctrlKey,
        };
    }
    /*private*/ _key_event(e) {
        return {
            type: e.type,
            keyCode: e.keyCode,
        };
    }
    /*private*/ _pan_start(e) {
        const ev = this._pan_event(e);
        // back out delta to get original center point
        ev.sx -= e.deltaX;
        ev.sy -= e.deltaY;
        this._trigger(this.pan_start, ev, e.srcEvent);
    }
    /*private*/ _pan(e) {
        this._trigger(this.pan, this._pan_event(e), e.srcEvent);
    }
    /*private*/ _pan_end(e) {
        this._trigger(this.pan_end, this._pan_event(e), e.srcEvent);
    }
    /*private*/ _pinch_start(e) {
        this._trigger(this.pinch_start, this._pinch_event(e), e.srcEvent);
    }
    /*private*/ _pinch(e) {
        this._trigger(this.pinch, this._pinch_event(e), e.srcEvent);
    }
    /*private*/ _pinch_end(e) {
        this._trigger(this.pinch_end, this._pinch_event(e), e.srcEvent);
    }
    /*private*/ _rotate_start(e) {
        this._trigger(this.rotate_start, this._rotate_event(e), e.srcEvent);
    }
    /*private*/ _rotate(e) {
        this._trigger(this.rotate, this._rotate_event(e), e.srcEvent);
    }
    /*private*/ _rotate_end(e) {
        this._trigger(this.rotate_end, this._rotate_event(e), e.srcEvent);
    }
    /*private*/ _tap(e) {
        this._trigger(this.tap, this._tap_event(e), e.srcEvent);
    }
    /*private*/ _doubletap(e) {
        this._trigger(this.doubletap, this._tap_event(e), e.srcEvent);
    }
    /*private*/ _press(e) {
        this._trigger(this.press, this._tap_event(e), e.srcEvent);
    }
    /*private*/ _pressup(e) {
        this._trigger(this.pressup, this._tap_event(e), e.srcEvent);
    }
    /*private*/ _mouse_enter(e) {
        this._trigger(this.move_enter, this._move_event(e), e);
    }
    /*private*/ _mouse_move(e) {
        this._trigger(this.move, this._move_event(e), e);
    }
    /*private*/ _mouse_exit(e) {
        this._trigger(this.move_exit, this._move_event(e), e);
    }
    /*private*/ _mouse_wheel(e) {
        this._trigger(this.scroll, this._scroll_event(e), e);
    }
    /*private*/ _context_menu(_e) {
        // TODO
    }
    /*private*/ _key_down(e) {
        // NOTE: keyup event triggered unconditionally
        this.trigger(this.keydown, this._key_event(e));
    }
    /*private*/ _key_up(e) {
        // NOTE: keyup event triggered unconditionally
        this.trigger(this.keyup, this._key_event(e));
    }
}
UIEventBus.__name__ = "UIEventBus";
//# sourceMappingURL=ui_events.js.map