var _a;
import { Filter } from "./filter";
import { Indices } from "../../core/types";
export class UnionFilter extends Filter {
    constructor(attrs) {
        super(attrs);
    }
    compute_indices(source) {
        const { operands } = this;
        if (operands.length == 0) {
            const size = source.get_length() ?? 1;
            return Indices.all_set(size);
        }
        else {
            const [index, ...rest] = operands.map((op) => op.compute_indices(source));
            for (const op of rest) {
                index.add(op);
            }
            return index;
        }
    }
}
_a = UnionFilter;
UnionFilter.__name__ = "UnionFilter";
(() => {
    _a.define(({ Array, Ref }) => ({
        operands: [Array(Ref(Filter))],
    }));
})();
//# sourceMappingURL=union_filter.js.map