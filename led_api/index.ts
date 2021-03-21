import envs from "./envs";
import express from "express";
import bodyParser from "body-parser";
import magic from "magic-home";
import {checkEffectsArray} from "./effectDeclarations";
import LEDEffectController from "./LEDEffectController";
import {isJson} from "./utils";


const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

const LEDS = JSON.parse(envs.leds);
const ACK = JSON.parse(envs.ack);
const CONTROLLERS : Record<string, LEDEffectController> = {};
for (const [name, ip] of Object.entries(LEDS)) {
    CONTROLLERS[name] = new LEDEffectController(new magic.Control(ip, { ack: ACK }), parseInt(envs.checkChangedStateInterval));
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
 *     speed: number, // speed of the effect. Must be between 0 and 100
 *     power: bool (optional), // if power should be on or off. Default: on. optional
 *     rgb: [0-255,0-255,0-255] (optional unless color === rgb), // rgb value for the color. only needed, if color === rgb
 * }
 * The duration of the last effect will be ignored (it will be indefinitely with priority 0)
 */
app.post("/effect", async function(req, res) {
    const name = req.body?.name;
    if (name in CONTROLLERS) {
        const controller = CONTROLLERS[name];
        if (controller.priority <= req.body.priority) {
            if (isJson(req.body.effects)) {
                const effects = JSON.parse(req.body.effects);
                if (checkEffectsArray(effects)) {
                    controller.overrideQueue(effects).then(); // empty then. Otherwise PHP Storm complaints
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
