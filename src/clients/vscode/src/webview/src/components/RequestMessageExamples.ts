
export default class RequestMessageExamples {

    private examples = {

        'get': `
// this is a comment and comment can be mark as '#' or '//'

GET https://eovogku1ema9d9b.m.pipedream.net/user/id/{{ string }} HTTP/1.1

###

# GET is the default verb
https://example.com/comments/{{ digit }} 

###

GET https://example.com/topics/{{ string }} HTTP/1.1
        `,

        'post': `
POST https://example.com/comments HTTP/1.1
content-type: application/json

{
    "name": "{{ username }}",
    "time": "{{ datetime }}"
}
`

    };

    public loadExample(key = 'get'): string {
        return this.examples[key];
    }
}