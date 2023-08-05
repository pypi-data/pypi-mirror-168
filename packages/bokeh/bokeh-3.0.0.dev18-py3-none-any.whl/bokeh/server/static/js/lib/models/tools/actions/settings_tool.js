var _a;
import { ActionTool, ActionToolView } from "./action_tool";
import * as icons from "../../../styles/icons.css";
import { Dialog } from "../../ui/dialog";
import { Inspector } from "../../ui/inspector";
import { build_view } from "../../../core/build_views";
export class SettingsToolView extends ActionToolView {
    async lazy_initialize() {
        await super.lazy_initialize();
        const dialog = new Dialog({
            content: new Inspector({ target: this.parent.model }),
            closable: true,
            visible: false,
        });
        this._dialog = await build_view(dialog, { parent: this.parent });
    }
    doit() {
        this._dialog.model.visible = true;
    }
}
SettingsToolView.__name__ = "SettingsToolView";
export class SettingsTool extends ActionTool {
    constructor(attrs) {
        super(attrs);
        this.tool_name = "Settings";
        this.tool_icon = icons.tool_icon_settings;
    }
}
_a = SettingsTool;
SettingsTool.__name__ = "SettingsTool";
(() => {
    _a.prototype.default_view = SettingsToolView;
    _a.register_alias("settings", () => new SettingsTool());
})();
//# sourceMappingURL=settings_tool.js.map