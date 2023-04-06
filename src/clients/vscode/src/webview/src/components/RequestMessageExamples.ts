
export default class RequestMessageExamples {

    private fileupload = {
        'file-upload-myfile-batchfile': `
// content align to left with no trailing spaces between "" so that file content will not have trailing whitespaces either

POST https://httpbin.org/post
x-ms-blob-type: BlockBlob

{{
'

string,username,password,filename,datetime
{{string}},{{username}},{{password}},{{filename}},{{datetime}}
{{string}},{{username}},{{password}},{{filename}},{{datetime}}
{{string}},{{username}},{{password}},{{filename}},{{datetime}}
{{string}},{{username}},{{password}},{{filename}},{{datetime}}
{{string}},{{username}},{{password}},{{filename}},{{datetime}}
{{string}},{{username}},{{password}},{{filename}},{{datetime}}

'
| myfile("batchfile.log")
}}
    
    `,

    'file-upload-myfile-json': `
// this is a custom file content
// supports with multi breakline

POST https://httpbin.org/post
    
{{
'

{
    \\"name\\": \\"{{ string }}\\",
    \\"age\\": \\"{{ digit }}\\"
}

' | myfile("filename.txt")
}}
        `,
    
    'file-upload-myfile-wordlisttypes': `
    
// custom file content supports primitive wordlists

POST https://httpbin.org/post
    
{{

'

{{ string }}
{{ sqlinject }}
{{ xss }}
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

'

| myfile("filename.txt")
}}
            `,
    }
    
    private graphql = {
        'gql-mutation-mutate-var-1':
`
POST https://graphqlzero.almansi.me/api
X-REQUEST-TYPE: GraphQL

mutation (
  $id: ID!,
  $input: UpdatePostInput!
) {
  updatePost(id: $id, input: $input) {
    id
    body
  }
}

{
  "id": 1,
  "input": {
    "body": "{{ string }}"
  }
}
`,

    'gql-query-1':
`
POST https://rickandmortyapi.com/graphql
X-REQUEST-TYPE: GraphQL

query MyQuery {
    character(id: "{{ digit }}") {
      id
      gender
      name
      species
      status
      type
      origin {
        dimension
        name
        created
      }
    }
  }
`
    }

    private post = {
        
        'post-json': `
POST https://httpbin.org/post HTTP/1.1
Content-Type: application/json

{
    "name": "{{ username }}",
    "time": "{{ datetime }}",
    "age": "{{ digit }}"
}
`,
        'post-xwwwformurlencoded': `
POST https://httpbin.org/post HTTP/1.1
Content-Type: application/x-www-form-urlencoded

name=foo
&password=bar
`,

'post-file': `
POST https://httpbin.org/post HTTP/1.1

{{ file('option-file-name.log') }}
`,

'post-pdf': `
POST https://httpbin.org/post HTTP/1.1

{{ pdf('option-file-name.pdf') }}
`,

'post-image': `
POST https://httpbin.org/post HTTP/1.1

{{ image('option-file-name.png') }}
`,

'post-xml':`
POST https://httpbin.org/post HTTP/1.1
Content-Type: application/xml
Authorization: {{ string }}

<request>
    <name>{{ username }}</name>
    <time>{{ datetime }}</time>
</request>
`,

'post-html-xss':`
POST https://httpbin.org/post HTTP/1.1

<html>
 <body>
  <div>Welcome <p> <script>{{ xss }}</script> </p></div>
 </body>
</html>
`
    }

    private get = {

        'get-multiple-1': `
// this is a comment and comment can be mark as '#' or '//'
// some definitions from 
//   -request-line = Verb(default GET) + (protocol + hostname) + path + querystring
//   -each ### is a delimiter for a request-block and below has 4 request-blocks

GET https://httpbin.org/user/id/{{ string }} HTTP/1.1

###

# GET is the default verb
https://httpbin.org/comments/{{ digit }} 

###

https://httpbin.org/get
            ?name={{username}}&address={{string}}

###

GET https://httpbin.org/get
?name={{username}}
&address={{string}}
&order=5
&mode={{string}}

###

// headers must be on a newline after "request-line"

GET https://httpbin.org/get
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
    
    'get-path':
`
GET https://httpbin.org/links/{{ string }}/{{ bool }}/{{ digit }}/{{ integer }}/{{ char }}/{{ filename }}/{{ datetime }}/{{ date }}/{{ time }}/{{ username }}/{{ password }}
`,

    'get-path-qs':
`
GET https://httpbin.org/get
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
    'get-path-mutate-1':
`
GET https://httpbin.org/links?orderid={{ '12315' | mutate }}
`,

'get-discovery-path-qs':
`
GET https://httpbin.org/{{ httppath }}
`,

'get-with-random-qs-1':
`
GET https://httpbin.org/get
?name={{ ['James', 'Bobby', 'Keigo', 'Hans'] | random }}
&address={{ ['never', 'give' , 'up', 'never', 'stop', 'believing'] | random }}
&order={{ [1, 3 ,100, 32, 13, 22, 55, 'and', 'some', 'mix', 'of some words'] | random }}
`

    };

    private misc = {
        
        'misc-mutate-post':
`
POST https://httpbin.org/post
Content-Type: application/json

{
    "name": "john doe",
    "info": {{ 'this custom input will be mutated by fuzzie' | mutate }}
}

###

POST https://httpbin.org/post
Content-Type: application/xml

<note>
    <to>{{ username }}</to>
    <from>{{ username }}</from>
    <heading>{{ 'Reminder' | mutate }}</heading>
    <body>{{ 'Don\\'t forget me this weekend!' | mutate }}</body>
</note>

`,

'misc-http-port-scan':
`
//HTTP port scanning

{% set scheme = 'https://' %}
{% set hostname = 'httpbin.org' %}

GET {{scheme}}{{domain}}:{{ numrange(0,65536) }}/
`,

 'misc-variables-1':
 `
{% set htmlOpen = '<html><body><div>' %}
{% set htmlClose = '</div</body><html>' %}

POST https://httpbin.org/post HTTP/1.1

{{ htmlOpen }}
<p> Welcome <p> <script>{{ xss }}</script> </p>
{{ htmlClose }}

 `
 
    }

    public loadExample(key = 'get'): string {

        const keyType = key.split('-')[0];

        switch(keyType.toLowerCase()) {
            case 'file':
                return this.fileupload[key];
            case 'get':
                return this.get[key];
            case 'post':
                return this.post[key];
            case 'misc':
                return this.misc[key];
            case 'gql':
                return this.graphql[key];
        }

        return '';
    }
}