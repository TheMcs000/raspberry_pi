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
        if(this.currentTimeout !== undefined) {
            clearTimeout(this.currentTimeout);
        }
        this.queue.clear();

        const time = getTime();
        if(this.queue.size() === 0 && time > this.previousEffectGetTime + this.checkChangedStateInterval) {
            const currentEffect = await this.getCurrentLEDEffect();
            if (currentEffect !== undefined && (this.previousEffect === undefined || currentEffect.effectType !== EFFECT_TYPE.custom || !deepEquals(this.previousEffect.rgb,currentEffect.rgb))) {
                this.previousEffect = currentEffect;
            }
        }

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
            this.replacePreviousInEffect(effect, true); // inPlace is true
            this.executeEffect(effect, true);

            if(this.queue.size() > 0) {
                this.currentTimeout = setTimeout(function () {
                    o.startEffectQueue();
                }, effect.duration);
            } else { // queue is empty. this effect stays and must become previousEffect
                // this is safe, because @see replacePreviousInEffect
                this.previousEffect = effect;
            }
        } // else: queue is empty
    }

    /**
     * replaces previous effectType, color and so on
     * @param effect
     * @param inPlace if the effect should be changed in place or not
     * @private
     */
    private replacePreviousInEffect(effect: EFFECT, inPlace = false) : EFFECT {
        if(!inPlace) {
            effect = { ...effect };
        }

        // effectType
        if (effect.effectType === EFFECT_TYPE.previous) {
            if(this.previousEffect !== undefined) {
                effect.effectType = this.previousEffect.effectType;
            } else {
                effect.effectType = EFFECT_TYPE.static;
                MY_LOG.error("Cant replace previous effect type, because this.previousEffect is not defined");
            }
        }

        // color
        if (effect.color === COLOR.previous || effect.color === COLOR.previousDarken) {
            if(this.previousEffect !== undefined && this.previousEffect.rgb !== undefined) {
                if(effect.color === COLOR.previous) {
                    effect.rgb = this.previousEffect.rgb;
                } else { // effect.color === COLOR.previousDarken
                    const prevRGB = this.previousEffect.rgb;
                    effect.rgb = [prevRGB[0] / 2, prevRGB[1] / 2, prevRGB[2] / 2];
                }
            } else {
                effect.rgb = [255, 255, 255];
                MY_LOG.error("Cant replace previous color, because this.previousEffect or previous rgb is not defined");
            }
            effect.color = COLOR.rgb;
        }

        return effect;
    }

    /**
     * executes an effect. Does not care about duration
     * @param effect
     * @param previousReplaced if all previous stuff (like effectType, color, ...) already got replace
     */
    public executeEffect(effect: EFFECT, previousReplaced = false): void {
        console.log(effect);
        if(!previousReplaced) {
            effect = this.replacePreviousInEffect(effect);
        }
        if(effect.rgb !== undefined) {
            if ((effect.effectType === EFFECT_TYPE.static || effect.effectType === EFFECT_TYPE.custom)) {
                this.control.setColor(...effect.rgb);
            } else if (effect.effectType === EFFECT_TYPE.sweep) {
                const my_effect = new magic.CustomMode();

                my_effect
                    .addColor(...effect.rgb)
                    .addColor(effect.rgb[0] / 2, effect.rgb[1] / 2, effect.rgb[2] / 2)
                    .setTransitionType("fade");

                this.control.setCustomPattern(my_effect, effect.speed).catch(function (err: Error) {
                    MY_LOG.error("setCustomPattern failed", err);
                });
            } else {
                MY_LOG.error(`Unknown effect "${effect.effectType}" or insufficient parameters`);
            }
        } else {
            MY_LOG.error("the RGB is not set on this effect");
        }

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
