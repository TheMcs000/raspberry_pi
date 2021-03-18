import path from "path";
import dotenv = require("dotenv");
import {DotenvParseOutput} from "dotenv";

const GENERAL_CONFIG_PATH = path.resolve(process.cwd(), ".env");
const SPECIFIC_CONFIG_PATH = path.resolve(process.cwd(), ".env.local");

let envs: DotenvParseOutput;

const generalConfig = dotenv.config({
    path: GENERAL_CONFIG_PATH,
});
if(generalConfig.parsed === undefined) {
    throw "the .env file " + GENERAL_CONFIG_PATH + " could not be parsed and is mandatory. Error:" + generalConfig.error;
}

const specificConfig = dotenv.config({
        path: SPECIFIC_CONFIG_PATH,
    });
if(specificConfig.parsed === undefined) {
    console.warn("The .env file " + SPECIFIC_CONFIG_PATH + " could not be parsed. This is NOT critical");
    envs = generalConfig.parsed;
} else {
    envs = mergeObjectsNotDeep(specificConfig.parsed, generalConfig.parsed);
}


/**
 * Will merge the keys of two objects, where one object is dominant (this value will survive, if there is a key-collision).
 * Will only look on top level: Wont go into inner objects, trying to merge these. Will always override top keys
 * @param dominant the dominant object (every value will survive). WARNING: WILL BE MODIFIED
 * @param extraObject the non dominant object (value might be overridden by dominant)
 */
function mergeObjectsNotDeep(dominant: DotenvParseOutput, extraObject: DotenvParseOutput): DotenvParseOutput {
    for (const key of Object.keys(extraObject)) {
        if (dominant[key] === undefined) {
            dominant[key] = extraObject[key];
        }
    }
    return dominant;
}

export default envs;
