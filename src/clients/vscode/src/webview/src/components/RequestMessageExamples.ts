
export default class RequestMessageExamples {

    private fileupload = {
        'file-upload-myfile-batchfile': `
// content align to left with no trailing spaces between "" so that file content will not have trailing whitespaces either

PUT https://httpbin.org/post
x-ms-blob-type: BlockBlob

{{
"string,username,password,filename,datetime
{{string}},{{username}},{{password}},{{filename}},{{datetime}}
{{string}},{{username}},{{password}},{{filename}},{{datetime}}
{{string}},{{username}},{{password}},{{filename}},{{datetime}}
{{string}},{{username}},{{password}},{{filename}},{{datetime}}
{{string}},{{username}},{{password}},{{filename}},{{datetime}}
{{string}},{{username}},{{password}},{{filename}},{{datetime}}"
| myfile("batchfile_1.log")
}}
    
    `,

    'file-upload-myfile-json': `
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
    
    'file-upload-myfile-wordlisttypes': `
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
    }
    
    private graphql = {

    }

    private post = {
        
        'post': `
POST https://example.com/comments HTTP/1.1
content-type: application/json

{
    "name": "{{ username }}",
    "time": "{{ datetime }}"
}`
    }

    private get = {

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



    

    };

    public loadExample(key = 'get'): string {

        switch(key) {
            case 'file-upload-myfile-batchfile':
                return this.fileupload['file-upload-myfile-batchfile'];
            case 'file-upload-myfile-wordlisttypes':
                return this.fileupload['file-upload-myfile-wordlisttypes'];
            case 'file-upload-myfile-json':
                return this.fileupload['file-upload-myfile-json'];
            case 'get':
                return this.get['get'];
            case 'post':
                return this.post['post'];
            default:
              // code block
        }

        if (key == 'file-upload-file-myfile-batchfile') {
            return this.fileupload['file-upload-file-myfile-batchfile'];
        }

        return '';
    }
}