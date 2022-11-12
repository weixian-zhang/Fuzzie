

export default class Utils
{
    public static async readFileAsText(file): Promise<string>
    {
        return new Promise((resolve, reject) => {
            var reader = new FileReader();  
            reader.onload = (res) => {
                if(res != null)
                {
                   const result: string = res.target?.result as string;
                   resolve(result);
                
            }
            reader.onerror = (err) => {
                reject;
                //TODO: log
                console.log(err)
            }
            
            }
            reader.readAsText(file);
        })
    }
}