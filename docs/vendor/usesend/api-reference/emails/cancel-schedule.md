> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Cancel schedule



## OpenAPI

````yaml post /v1/emails/{emailId}/cancel
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/emails/{emailId}/cancel:
    post:
      parameters:
        - schema:
            type: string
            minLength: 3
            example: cuiwqdj74rygf74
          required: true
          name: emailId
          in: path
      responses:
        '200':
          description: Retrieve the user
          content:
            application/json:
              schema:
                type: object
                properties:
                  emailId:
                    type: string

````