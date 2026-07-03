> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Delete contact



## OpenAPI

````yaml delete /v1/contactBooks/{contactBookId}/contacts/{contactId}
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/contactBooks/{contactBookId}/contacts/{contactId}:
    delete:
      parameters:
        - schema:
            type: string
            example: cuiwqdj74rygf74
          required: true
          name: contactBookId
          in: path
        - schema:
            type: string
            example: cuiwqdj74rygf74
          required: true
          name: contactId
          in: path
      responses:
        '200':
          description: Contact deleted successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                required:
                  - success

````