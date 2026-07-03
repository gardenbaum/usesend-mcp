> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Bulk create contact



## OpenAPI

````yaml post /v1/contactBooks/{contactBookId}/contacts/bulk
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/contactBooks/{contactBookId}/contacts/bulk:
    post:
      parameters:
        - schema:
            type: string
            minLength: 3
            example: cuiwqdj74rygf74
          required: true
          name: contactBookId
          in: path
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  email:
                    type: string
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
                required:
                  - email
              maxItems: 1000
      responses:
        '200':
          description: Bulk add contacts to a contact book
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                  count:
                    type: number
                required:
                  - message
                  - count

````