import { range as arange } from "./array";
import { assert } from "./assert";
const { abs, ceil, max } = Math;
export function* range(start, stop, step = 1) {
    assert(step > 0);
    if (stop == null) {
        stop = start;
        start = 0;
    }
    const delta = start <= stop ? step : -step;
    const length = max(ceil(abs(stop - start) / step), 0);
    for (let i = 0; i < length; i++, start += delta) {
        yield start;
    }
}
export function* reverse(array) {
    const n = array.length;
    for (let i = 0; i < n; i++) {
        yield array[n - i - 1];
    }
}
export function* enumerate(seq) {
    let i = 0;
    for (const item of seq) {
        yield [item, i++];
    }
}
export function* skip(seq, n) {
    assert(n >= 0);
    for (const value of seq) {
        if (n == 0)
            yield value;
        else
            n -= 1;
    }
}
export function* tail(seq) {
    yield* skip(seq, 1);
}
export function* join(seq, separator) {
    let first = true;
    for (const entry of seq) {
        if (first)
            first = false;
        else if (separator != null)
            yield separator();
        yield* entry;
    }
}
export function* interleave(seq, separator) {
    let first = true;
    for (const entry of seq) {
        if (first)
            first = false;
        else
            yield separator();
        yield entry;
    }
}
export function* map(iterable, fn) {
    let i = 0;
    for (const item of iterable) {
        yield fn(item, i++);
    }
}
export function* flat_map(iterable, fn) {
    let i = 0;
    for (const item of iterable) {
        yield* fn(item, i++);
    }
}
export function every(iterable, predicate) {
    for (const item of iterable) {
        if (!predicate(item))
            return false;
    }
    return true;
}
export function some(iterable, predicate) {
    for (const item of iterable) {
        if (predicate(item))
            return true;
    }
    return false;
}
// https://docs.python.org/3.8/library/itertools.html#itertools.combinations
export function* combinations(seq, r) {
    const n = seq.length;
    if (r > n)
        return;
    const indices = arange(r);
    yield indices.map((i) => seq[i]);
    while (true) {
        let k;
        for (const i of reverse(arange(r))) {
            if (indices[i] != i + n - r) {
                k = i;
                break;
            }
        }
        if (k == null)
            return;
        indices[k] += 1;
        for (const j of arange(k + 1, r)) {
            indices[j] = indices[j - 1] + 1;
        }
        yield indices.map((i) => seq[i]);
    }
}
export function* subsets(seq) {
    for (const k of arange(seq.length + 1)) {
        yield* combinations(seq, k);
    }
}
//# sourceMappingURL=iterator.js.map