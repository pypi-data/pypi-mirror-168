const channel = new MessageChannel();
const tasks = new Map();
channel.port1.onmessage = (event) => {
    const handle = event.data;
    const fn = tasks.get(handle);
    if (fn != null) {
        try {
            fn();
        }
        finally {
            tasks.delete(handle);
        }
    }
};
let counter = 1;
export function defer() {
    return new Promise((resolve) => {
        const handle = counter++;
        tasks.set(handle, resolve);
        channel.port2.postMessage(handle);
    });
}
export function delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}
export function paint() {
    return new Promise((resolve) => {
        requestAnimationFrame(() => resolve());
    });
}
export function idle() {
    return new Promise((resolve) => {
        requestIdleCallback(() => resolve());
    });
}
//# sourceMappingURL=defer.js.map