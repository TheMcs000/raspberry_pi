// the value must be the same as the key!
export enum EFFECT_TYPE {
    previous="previous", // the same effect the LED was before the API call
    static="static", // the color lights normally
    sweep="sweep", // like pulsing, but it doesnt turn off completely
}

// the value must be the same as the key!
export enum COLOR {
    previous="previous", // the same color the LED was before the API call
    rgb="rgb", // rgb value supplied by API in the rgb field
}

export interface EFFECT {
    effectType: EFFECT_TYPE,
    color: COLOR,
    duration: number,
    power?: boolean,
    speed?: number,
    rgb?: [number,number,number],
}

/**
 * Checks if object is instance of @see EffectDeclarations
 * @param object the object that should be checked
 */
export function instanceOfEFFECT(object: Record<string, any>): object is EFFECT {
    return object.effectType in EFFECT_TYPE &&
        object.color in COLOR &&
        typeof object.duration === "number" && object.duration > 0 &&
        (!("power" in object) || typeof object.power === "boolean") &&
        (!("speed" in object) || (typeof object.speed === "number" && object.speed >= 0 && object.speed <= 100)) &&
        (object.color !== "rgb" || (Array.isArray(object.rgb) && object.rgb.length === 3 &&
            typeof object.rgb[0] === "number" && object.rgb[0] >= 0 && object.rgb[0] <= 255 &&
            typeof object.rgb[1] === "number" && object.rgb[1] >= 0 && object.rgb[1] <= 255 &&
            typeof object.rgb[2] === "number" && object.rgb[2] >= 0 && object.rgb[2] <= 255));
}

/**
 * checks if given input is a valid effects array, or not
 * @param userInput
 */
export function checkEffectsArray(userInput: unknown): userInput is Array<EFFECT> {
    if(Array.isArray(userInput)) {
        for (const effect of userInput) {
            if(!instanceOfEFFECT(effect)) {
                return false;
            }
        }
        return true;
    } else {
        return false;
    }
}
