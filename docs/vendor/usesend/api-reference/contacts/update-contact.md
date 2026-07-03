> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Update contact



## OpenAPI

````yaml patch /v1/contactBooks/{contactBookId}/contacts/{contactId}
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/contactBooks/{contactBookId}/contacts/{contactId}:
    patch:
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
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                firstName:
                  type: string
                lastName:
                  type: string
                properties:
                  type: object
                  additionalProperties:
                    type: string
                subscribed:
                  type: boolean
      responses:
        '200':
          description: Retrieve the user
          content:
            application/json:
              schema:
                type: object
                properties:
                  contactId:
                    type: string

````