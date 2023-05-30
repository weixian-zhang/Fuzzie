
import {ChildProcess} from "child_process";

export class AppContext
{
    fuzzerPath = ""
    fuzzerDistFolder: string = "";
    fuzzerUnzippedFolder = "";
    fuzzerPYZFilePath: string = "";
    pythonChildProcess: ChildProcess = new ChildProcess();
    sqliteFilePath: string = "";
}