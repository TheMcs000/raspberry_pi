import envs from "./envs";
import express from "express";
import * as magic from "magic-home";
const app = express();

const light = new magic.Control("192.168.0.188");
light.setPower(true);

app.get("/", (req, res) => {
    res.send("Hello World!");
});

app.listen(envs.port, () => {
    console.log(`Example app listening at http://localhost:${envs.port}`);
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
