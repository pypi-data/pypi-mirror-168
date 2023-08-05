import { BBox } from "./bbox";
import { OutputBackend } from "../enums";
export declare type CanvasPatternRepetition = "repeat" | "repeat-x" | "repeat-y" | "no-repeat";
export declare type Context2d = {
    createPattern(image: CanvasImageSource, repetition: CanvasPatternRepetition | null): CanvasPattern | null;
    setImageSmoothingEnabled(value: boolean): void;
    getImageSmoothingEnabled(): boolean;
    lineDash: number[];
    readonly layer: CanvasLayer;
} & CanvasRenderingContext2D;
export declare class CanvasLayer {
    readonly backend: OutputBackend;
    readonly hidpi: boolean;
    private readonly _canvas;
    get canvas(): HTMLCanvasElement;
    private readonly _ctx;
    get ctx(): Context2d;
    private readonly _el;
    get el(): HTMLElement;
    readonly pixel_ratio: number;
    bbox: BBox;
    constructor(backend: OutputBackend, hidpi: boolean);
    resize(width: number, height: number): void;
    private get target();
    private _base_transform;
    undo_transform(fn: (ctx: Context2d) => void): void;
    prepare(): void;
    clear(): void;
    finish(): void;
    to_blob(): Promise<Blob>;
}
//# sourceMappingURL=canvas.d.ts.map