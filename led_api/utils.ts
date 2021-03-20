/**
 * You can await this. it will resolve after time (always resolves, never rejects)
 * @param time time to wait (unit: ms)
 */
export function wait(time: number): Promise<void> {
    return new Promise<void>(function (resolve) {
        setTimeout(function () {
            resolve();
        }, time);
    });
}

/**
 * checks if str is a valid json
 * @param str
 */
export function isJson(str: string): boolean {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}

/**
 * Gets the current time in milliseconds
 */
export function getTime() : number {
    return (new Date()).getTime();
}

/**
 * If two elements (any type) a and b are deeply compared equal
 * @param a element a
 * @param b element b
 */
export function deepEquals(a: unknown,b: unknown) : boolean {
    if(typeof a === typeof b && Array.isArray(a) === Array.isArray(b)) {
        if(typeof a === "object" && a !== null && b !== null) {
            if(Array.isArray(a)) {
                // @ts-ignore ts is not smart: above checks that 'b' is like 'a'
                if(a.length != b.length) {
                    return false;
                }
                for(let i = 0; i < a.length; i++) {
                    // @ts-ignore ts is not smart: above checks that 'b' is like 'a'
                    if(deepEquals(a[i],b[i])) {
                        return false;
                    }
                }
                return true;
            } else {
                const keysA = Object.keys(a);
                // @ts-ignore ts is not smart: above checks that 'b' is like 'a'
                const keysB = Object.keys(b);
                if(keysA.length != keysB.length) {
                    return false;
                }
                for(let i = 0; i < keysA.length; i++) {
                    // @ts-ignore weird type casting of unknown
                    if(keysA[i] != keysB[i] || !deepEquals(a[keysA[i]], b[keysA[i]])) {
                        return false;
                    }
                }
                return true;
            }
        } else {
            return a == b;
        }
    }
    return false;
}
