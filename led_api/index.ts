import envs from "./envs";
import express from "express";
import * as bodyParser from "body-parser";
import * as magic from "magic-home";
import {checkEffectsArray, COLOR, EFFECT, EFFECT_TYPE} from "./effectDeclarations";
import Queue from "./Queue";
import {clearTimeout} from "timers";
import executeEffect from "./executeEffect";
import {MY_LOG} from "./MY_LOG";
import Timeout = NodeJS.Timeout;


const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

const CURRENT_EFFECT_TIMEOUTS: Record<string, Timeout> = {};
const EFFECT_QUEUES: Record<string, Queue<META_EFFECT>> = {};

const LEDS = JSON.parse(envs.leds);
const ACK = JSON.parse(envs.ack);
const CONTROLLERS : Record<string, magic.Control> = {};
for (const [name, ip] of Object.entries(LEDS)) {
    CONTROLLERS[name] = new magic.Control(ip, { ack: ACK });
    EFFECT_QUEUES[name] = new Queue<META_EFFECT>();
    // getCurrentLEDEffect(CONTROLLERS[name]).then((x) => console.log(x));
}

interface META_EFFECT {
    control: magic.Control,
    priority: number,
    effect: EFFECT,
}

/**
 * API definition:
 * name: string, // name of the LED. Look into the .env file for defined names
 * priority: number, // priority of this effect. if a effect with > priority is running, this request will be ignored (and the result will be 423 locked)
 * effects - Array of effects. One effect looks like this:
 * {
 *     effectType: enum, // @see EFFECT_TYPE
 *     color: enum, // see color enum
 *     duration: number, // duration of the effect in ms. Must be > 0
 *     power: bool (optional), // if power should be on or off. Default: on. optional
 *     speed: number (optional), // speed of the effect. Must be between 0 and 100. Should only be set, if you want to override a default effect. optional
 *     rgb: [0-255,0-255,0-255] (if color === rgb), // rgb value for the color. only needed, if color === rgb
 * }
 * The duration of the last effect will be ignored (it will be indefinitely with priority 0)
 */
app.post("/effect", async function(req, res) {
    const name = req.body?.name;
    if (name in CONTROLLERS) {
        const queuePeek = EFFECT_QUEUES[name].peek();
        if (queuePeek === undefined || queuePeek.priority <= req.body.priority) {
            if (isJson(req.body.effects)) {
                const effects = JSON.parse(req.body.effects);
                if (checkEffectsArray(effects)) {
                    clearPendingEffects(name);
                    for (const effect of effects) {
                        EFFECT_QUEUES[name].push({
                            control: CONTROLLERS[name],
                            priority: req.body.priority,
                            effect: effect,
                        });
                    }
                    startEffectQueue(name);
                    res.sendStatus(200);
                } else {
                    res.sendStatus(400); // bad request
                }
            } else {
                res.sendStatus(400); // bad request
            }
        } else {
            res.sendStatus(423); // locked
        }
    } else {
        res.sendStatus(404); // not found
    }
});

app.get("/", async function(req, res) {
    res.send("Hello World!");
});

app.listen(envs.port, function() {
    console.log(`Listening at http://localhost:${envs.port}`);
});

/**
 * Clears all pending effects and clears the queue
 * @param name the name of the LED
 */
function clearPendingEffects(name: string) : void {
    clearTimeout(CURRENT_EFFECT_TIMEOUTS[name]);
    EFFECT_QUEUES[name].clear();
}

/**
 * Starts the effect queue
 * WARNING: NO OTHER TIMEOUT MAY BE RUNNING
 * @param name the name of the LED
 */
function startEffectQueue(name: string): void {
    const metaEffect = EFFECT_QUEUES[name].pop();
    if(metaEffect !== undefined) {
        // @ts-ignore I dont know why ts does not think that setTimeout returns a Timeout
        CURRENT_EFFECT_TIMEOUTS[name] = setTimeout(function () {
            startEffectQueue(name);
        }, metaEffect.effect.duration);
        executeEffect(metaEffect.control, metaEffect.effect);
    }
}

/**
 * Asks the controller for the current status and turns it into a @see EFFECT
 * @param control the controller of the LED
 */
function getCurrentLEDEffect(control: magic.Control) : Promise<undefined|EFFECT> {
    return new Promise<undefined|EFFECT>(function (resolve) {
        control.queryState(function (error: null|Error, state: any) {
            if (error !== null) { // then error
                MY_LOG.error("Cant get current LED Effect", error);
                resolve(undefined);
            } else { // then no error
                // console.log(state);
                // todo: for now the effectType is always static. Test with it, if user sets it via remote control
                resolve({
                    effectType: EFFECT_TYPE.static,
                    color: COLOR.rgb,
                    duration: 1000,
                    power: state.on,
                    rgb: [<number>state.color["red"], <number>state.color["green"], <number>state.color["blue"]],
                });
            }
        });
    });
}

/**
 * You can await this. it will resolve after time (always resolves, never rejects)
 * @param time time to wait (unit: ms)
 */
function wait(time: number): Promise<void> {
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
function isJson(str: string): boolean {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}
