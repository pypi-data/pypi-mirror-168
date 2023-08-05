import { ActionTool, ActionToolView } from "./action_tool";
import * as p from "../../../core/properties";
import { DialogView } from "../../ui/dialog";
export declare class SettingsToolView extends ActionToolView {
    model: SettingsTool;
    protected _dialog: DialogView;
    lazy_initialize(): Promise<void>;
    doit(): void;
}
export declare namespace SettingsTool {
    type Attrs = p.AttrsOf<Props>;
    type Props = ActionTool.Props;
}
export interface SettingsTool extends SettingsTool.Attrs {
}
export declare class SettingsTool extends ActionTool {
    properties: SettingsTool.Props;
    __view_type__: SettingsToolView;
    constructor(attrs?: Partial<SettingsTool.Attrs>);
    tool_name: string;
    tool_icon: string;
}
//# sourceMappingURL=settings_tool.d.ts.map