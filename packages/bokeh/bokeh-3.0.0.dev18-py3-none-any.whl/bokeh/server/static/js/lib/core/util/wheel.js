/*!
 * jQuery Mousewheel 3.1.13
 *
 * Copyright jQuery Foundation and other contributors
 * Released under the MIT license
 * http://jquery.org/license
 */
function fontSize(element) {
    const value = getComputedStyle(element).fontSize;
    const size = parseInt(value, 10);
    return isNaN(size) ? null : size;
}
function lineHeight(element) {
    const parent = element.offsetParent ?? document.body;
    return fontSize(parent) ?? fontSize(element) ?? 16;
}
function pageHeight(element) {
    return element.clientHeight; // XXX: should be content height?
}
export function getDeltaY(event) {
    let deltaY = -event.deltaY;
    if (event.target instanceof HTMLElement) {
        switch (event.deltaMode) {
            case event.DOM_DELTA_LINE:
                deltaY *= lineHeight(event.target);
                break;
            case event.DOM_DELTA_PAGE:
                deltaY *= pageHeight(event.target);
                break;
        }
    }
    return deltaY;
}
//# sourceMappingURL=wheel.js.map