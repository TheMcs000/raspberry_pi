/**
 * a logger which prints on the console and to a file
 */
class MyLog {
    private readonly logLevel: Level;

    public constructor(logLevel: Level) {
        this.logLevel = logLevel;
    }

    private handleStrings(level: Level, msg: Array<string|Error>) : void {
        if(level >= this.logLevel) {
            // todo: write to file
            // todo: more beautiful
            console.log(Level[level], MyLog.stackTrace());
            console.log(Level[level], ...msg);
        }
    }

    private static stackTrace() : string {
        const err = new Error();
        return <string>err.stack;
    }

    public info(...msg: string[]) : void {
        this.handleStrings(Level.INFO, msg);
    }

    public debug(...msg: string[]) : void {
        this.handleStrings(Level.DEBUG, msg);
    }

    public error(...msg: Array<string|Error>) : void {
        // todo: print type error beautiful
        this.handleStrings(Level.ERROR, msg);
    }

    public warn(msg: string[]) : void {
        this.handleStrings(Level.WARNING, msg);
    }

    public critical(msg: string[]) : void {
        this.handleStrings(Level.CRITICAL, msg);
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
}

enum Level {
    CRITICAL=50,
    ERROR=40,
    WARNING=30,
    INFO=20,
    DEBUG=10,
    NOT_SET=0,
}

export const MY_LOG = new MyLog(Level.NOT_SET);
