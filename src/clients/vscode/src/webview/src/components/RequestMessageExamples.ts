
export default class RequestMessageExamples {

    private examples = {

        'get': `
// this is a comment and comment can be mark as '#' or '//'
// some definitions from 
//   -request-line = Verb(default GET) + (protocol + hostname) + path + querystring
//   -each ### is a delimiter for a request-block and below has 4 request-blocks

GET https://eovogku1ema9d9b.m.pipedream.net/user/id/{{ string }} HTTP/1.1

###

# GET is the default verb
https://eovogku1ema9d9b.m.pipedream.net/comments/{{ digit }} 

###

https://httpbin.org/get
            ?name={{username}}&address={{string}}

###

GET https://eovogku1ema9d9b.m.pipedream.net
?name={{username}}
&address={{string}}
&order=5
&mode={{string}}

###

// headers must be on a newline after "request-line"

GET https://eovogku1ema9d9b.m.pipedream.net
?name={{username}}
&address={{string}}
&order=5
&mode={{string}}
Content-Type: application/xml
Authorization: {{ string }}
CustomHeader-1: {{ digit }}
CustomHeader-2: {{ filename }}
CustomHeader-3: {{ username }}
        `,




        'post': `
POST https://example.com/comments HTTP/1.1
content-type: application/json

{
    "name": "{{ username }}",
    "time": "{{ datetime }}"
}
`,

    'myfile-batchfile': `
POST https://httpbin.org/post
    
{{
    "
    string,username,password,filename,datetime
    {{string}},{{username}},{{password}},{{filename}},{{datetime}}
    {{string}},{{username}},{{password}},{{filename}},{{datetime}}
    {{string}},{{username}},{{password}},{{filename}},{{datetime}}
    {{string}},{{username}},{{password}},{{filename}},{{datetime}}
    {{string}},{{username}},{{password}},{{filename}},{{datetime}}
    {{string}},{{username}},{{password}},{{filename}},{{datetime}}
    "
    | myfile("batchfile_1.log")
}}
    `,

    'myfile-json': `
POST https://httpbin.org/post
    
{{
    "
    this is a custom file content
    supports with multi breakline
    
    {
        \\"name\\": \\"{{ string }}\\",
        \\"age\\": \\"{{ digit }}\\"
    }
    
    " | myfile("a-file.log")
}}
        `,
    
    'myfile-wordlisttypes': `
POST https://httpbin.org/post
    
{{
    "
    {{ string }}
    {{ bool }}
    {{ digit }}
    {{ integer }}
    {{ char }}
    {{ filename }}
    {{ datetime }}
    {{ date }}
    {{ time }}
    {{ username }}
    {{ password }}
    
    " | myfile("a-file.log")
}}
            `,

    };

    public loadExample(key = 'get'): string {
        return this.examples[key];
    }
}