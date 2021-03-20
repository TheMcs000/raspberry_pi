import * as magic from "magic-home";
import {EFFECT, EFFECT_TYPE} from "./effectDeclarations";


/**
 * executes an effect. Does not care about duration
 * @param control
 * @param effect
 */
export default function executeEffect(control : magic.Control, effect: EFFECT): void {
    if(effect.effectType === EFFECT_TYPE.static) {
        control.setColor(...effect.rgb);
    } else if(effect.effectType === EFFECT_TYPE.sweep) {
        const my_effect = new magic.CustomMode();

        my_effect
            .addColor(255, 0, 0)
            .addColor(100, 0, 0)
            .setTransitionType("fade");

        control.setCustomPattern(my_effect, 100).then((success: any) => {
            console.log((success) ? "success" : "failed");
        }).catch((err: any) => {
            console.log("Error:", err.message);
        });
    } else if(effect.effectType === EFFECT_TYPE.previous) {
        console.log("TODO: EFFECT PREVIOUS"); // todo: effect previous
    }

    control.setPower(effect.power !== false);
}
