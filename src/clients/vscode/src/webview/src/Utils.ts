

export default class Utils
{
    public static copy(obj: any) {
        if(obj == null || obj == undefined)
        {
            return null;
        }

        return JSON.parse(JSON.stringify(obj));
    }

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

    public static mapProp(source: any, target: any , skipPropIfTargetNotFound = true) {

        if(source == undefined)
        {
            return;
        }
        
        const thisObj = this;

        const keys = Object.keys( source )
        
        for (const key of keys) {
            if (source[ key ] == null)
                continue;
            if(Array.isArray(source[ key ] ))
                continue;
            else if ( typeof source[ key ] === 'object' ) {
                // If it's an object, let's go recursive
                thisObj.mapProp(source[ key ], target );
            }
            else {

                let srcVal = source[ key ];

                if(srcVal instanceof Number)
                {
                    srcVal = Number(srcVal);
                }

                if(skipPropIfTargetNotFound)
                {
                    if(key in target)
                    {
                        target[ key ] = srcVal;
                    }
                }
                else
                {
                    target[ key ] = srcVal;
                }
                
            }
        }
    }

    public static isValidHttpUrl(string) {
        let url;
        try {
          url = new URL(string);
        } catch (_) {
          return false;
        }
        return url.protocol === "http:" || url.protocol === "https:";
      }
}