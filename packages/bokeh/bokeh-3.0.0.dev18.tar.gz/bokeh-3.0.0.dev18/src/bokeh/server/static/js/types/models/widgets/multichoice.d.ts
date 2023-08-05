import Choices from "choices.js";
import { StyleSheetLike } from "../../core/dom";
import * as p from "../../core/properties";
import { InputWidget, InputWidgetView } from "./input_widget";
export declare class MultiChoiceView extends InputWidgetView {
    model: MultiChoice;
    input_el: HTMLSelectElement;
    choice_el: Choices;
    connect_signals(): void;
    styles(): StyleSheetLike[];
    render(): void;
    set_disabled(): void;
    change_input(): void;
}
export declare namespace MultiChoice {
    type Attrs = p.AttrsOf<Props>;
    type Props = InputWidget.Props & {
        value: p.Property<string[]>;
        options: p.Property<(string | [string, string])[]>;
        max_items: p.Property<number | null>;
        delete_button: p.Property<boolean>;
        placeholder: p.Property<string | null>;
        option_limit: p.Property<number | null>;
        search_option_limit: p.Property<number | null>;
        solid: p.Property<boolean>;
    };
}
export interface MultiChoice extends MultiChoice.Attrs {
}
export declare class MultiChoice extends InputWidget {
    properties: MultiChoice.Props;
    __view_type__: MultiChoiceView;
    constructor(attrs?: Partial<MultiChoice.Attrs>);
}
//# sourceMappingURL=multichoice.d.ts.map