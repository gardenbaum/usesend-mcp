> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Delete domain



## OpenAPI

````yaml delete /v1/domains/{id}
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/domains/{id}:
    delete:
      parameters:
        - schema:
            type: number
            nullable: true
            example: 1
          required: false
          name: id
          in: path
      responses:
        '200':
          description: Domain deleted successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: number
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
          description: Domain not found
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