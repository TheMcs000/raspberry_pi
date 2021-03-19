import envs from "./envs";
import express from "express";
import * as magic from "magic-home";
const app = express();

const light = new magic.Control("192.168.0.188");
light.setPower(true);

enum EFFECT {
    previous, // the same effect the LED was before the API call
    static, // the color lights normally
}

const my_effect = new magic.CustomMode();

my_effect
    .addColor(255, 0, 0)
    .addColor(100, 0, 0)
    .setTransitionType("fade");

light.setCustomPattern(my_effect, 100).then((success: any) => {
    console.log((success) ? "success" : "failed");
}).catch((err: any) => {
    return console.log("Error:", err.message);
});

/**
 * API definition:
 * name: string, // name of the LED. Look into the .env file for defined names
 * effects - Array of effects. One effect looks like this:
 * {
 *     effect: enum, // @see EFFECT
 *     priority: number, // if priority is >= than current effect, it will override. Otherwise it will be ignored. If previous was over priority level, it will override every time
 *     color: enum, // see color enum below
 *     duration: number, // duration of the effect in ms. If negative, it will be permanent. All effects afterwards will be ignored
 *     power: bool (optional), // if power should be on or off. Default: on. optional
 *     brightness: false|number (optional), // if false: does nothing. if number between 0 and 100: Sets the brightness by altering the RGB values (clamping the highest / lowest to 0 / 255). Default: false. optional
 * }
 *
 * color: {
 *     "previous" - the same color the LED was before the API call
 *     "rgb(R,G,B)" - rgb value
 * }
 */
app.get("/effect", (req, res) => {
    res.send("Hello World!");
});

app.get("/", (req, res) => {
    res.send("Hello World!");
});

app.listen(envs.port, () => {
    console.log(`Listening at http://localhost:${envs.port}`);
});

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

// /**
//  * Appends to log file
//  * @param content
//  */
// function log(content: string) {
//     fs.appendFile('log.txt',new Date().getTime() + ' --- ' + content + '\n', function (err) {
//         if (err) {
//             console.error(err);
//         }
//     });
// }
