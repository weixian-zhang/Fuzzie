
import WebClient from "./WebClient";

export default class FuzzerManager
{
    private webclient: WebClient;
    private isFuzzerWSConnected: boolean = false;
    private isFuzzerGraphQLRunning = true;
    
    public constructor()
    {
        this.webclient = new WebClient()
    }

    public async isFuzzerReady(): Promise<boolean>
    {
        this.isFuzzerWSConnected = await this.webclient.connectToFuzzerWSServer();

        return true;
        //is websocket connected

        //
    }

    public isFuzzerRunning(): Promise<boolean>
    {
        return new Promise<boolean>(false);
    }
}