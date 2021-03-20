/**
 * a queue class
 */
export default class Queue<T> {
    private _store: T[] = [];

    push(val: T): void {
        this._store.push(val);
    }

    peek(): T | undefined {
        return this._store[0];
    }

    pop(): T | undefined {
        return this._store.shift();
    }

    clear(): void {
        this._store = [];
    }
}
