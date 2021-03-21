import Queue from "./Queue";
import {COLOR, EFFECT, EFFECT_TYPE} from "./effectDeclarations";
import magic from "magic-home";
import {clearTimeout} from "timers";
import {MY_LOG} from "./MY_LOG";
import {deepEquals, getTime} from "./utils";
import Timeout = NodeJS.Timeout;

/**
 * handler for led effects
 */
export default class LEDEffectController {
    private currentTimeout : Timeout | undefined;
    private readonly queue = new Queue<EFFECT>();
    private previousEffectGetTime = 0;
    private previousEffect : undefined|EFFECT;
    private readonly control : magic.Control;
    private readonly checkChangedStateInterval : number;
    public priority = 0;


    constructor(control: magic.Control, checkChangedStateInterval : number) {
        this.control = control;
        this.checkChangedStateInterval = checkChangedStateInterval;
    }

    /**
     * Enqueues effects and overrides everything that was in the queue before
     * @param effects
     */
    public async overrideQueue(effects: EFFECT[]) : Promise<void> {
        const time = getTime();
        if(this.queue.size() === 0 && time > this.previousEffectGetTime + this.checkChangedStateInterval) {
            const currentEffect = await this.getCurrentLEDEffect();
            if (currentEffect !== undefined && (this.previousEffect === undefined || currentEffect.effectType !== EFFECT_TYPE.custom || !deepEquals(this.previousEffect.rgb,currentEffect.rgb))) {
                this.previousEffect = currentEffect;
            }
        }

        if(this.currentTimeout !== undefined) {
            clearTimeout(this.currentTimeout);
        }
        this.queue.clear();

        for (const effect of effects) {
            this.queue.push(effect);
        }
        this.startEffectQueue();
    }

    /**
     * Starts the effect queue
     */
    private startEffectQueue(): void {
        const o = this;
        const effect = this.queue.pop();
        if(effect !== undefined) {
            if(this.currentTimeout !== undefined) {
                clearTimeout(this.currentTimeout); // there shouldn't be a timeout running. But just to make sure
            }
            this.currentTimeout = setTimeout(function () {
                o.startEffectQueue();
            }, effect.duration);
            this.executeEffect(effect);
        }
    }

    /**
     * executes an effect. Does not care about duration
     * @param effect
     */
    public executeEffect(effect: EFFECT): void {
        if((effect.effectType === EFFECT_TYPE.static || effect.effectType === EFFECT_TYPE.custom) && Array.isArray(effect.rgb)) {
            this.control.setColor(...effect.rgb);
        } else if(effect.effectType === EFFECT_TYPE.sweep) {
            const my_effect = new magic.CustomMode();

            my_effect
                .addColor(255, 0, 0)
                .addColor(100, 0, 0)
                .setTransitionType("fade");

            this.control.setCustomPattern(my_effect, 100).then((success: any) => {
                console.log((success) ? "success" : "failed");
            }).catch((err: any) => {
                console.log("Error:", err.message);
            });
        } else if(effect.effectType === EFFECT_TYPE.previous) {
            console.log("TODO: EFFECT PREVIOUS"); // todo: effect previous
        }
        // todo: previous darken

        this.control.setPower(effect.power !== false);
    }

    /**
     * Asks the controller for the current status and turns it into a @see EFFECT
     */
    private getCurrentLEDEffect() : Promise<undefined|EFFECT> {
        const o = this;
        return new Promise<undefined|EFFECT>(function (resolve) {
            o.control.queryState(function (error: null|Error, state: any) {
                if (error !== null) { // then error
                    MY_LOG.error("Cant get current LED Effect", error);
                    resolve(undefined);
                } else { // then no error
                    // console.log(state);
                    let effectType = EFFECT_TYPE.static;
                    if(state.mode !== "color") {
                        effectType = EFFECT_TYPE.custom;
                    }

                    resolve({
                        effectType: effectType,
                        color: COLOR.rgb,
                        duration: 1000,
                        speed: state.speed,
                        power: state.on,
                        rgb: [<number>state.color["red"], <number>state.color["green"], <number>state.color["blue"]],
                    });
                }
            });
        });
    }
}
