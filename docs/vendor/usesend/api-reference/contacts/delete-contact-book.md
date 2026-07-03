> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Delete contact book



## OpenAPI

````yaml delete /v1/contactBooks/{contactBookId}
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/contactBooks/{contactBookId}:
    delete:
      parameters:
        - schema:
            type: string
            example: clx1234567890
          required: true
          name: contactBookId
          in: path
      responses:
        '200':
          description: Contact book deleted successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: string
                  success:
                    type: boolean
                  message:
                    type: string
                required:
                  - id
                  - success
                  - message
        '403':
          description: Forbidden - API key doesn't have access
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                required:
                  - error
        '404':
          description: Contact book not found
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                required:
                  - error

````