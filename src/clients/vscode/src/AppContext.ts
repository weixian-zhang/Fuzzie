
import {ChildProcess} from "child_process";

export class AppContext
{
    fuzzerPYZFolderPath: string = "";
    fuzzerPYZFilePath: string = "";
    pythonChildProcess: ChildProcess = new ChildProcess();
    sqliteFilePath: string = "";
}