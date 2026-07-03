> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Bulk delete contacts



## OpenAPI

````yaml delete /v1/contactBooks/{contactBookId}/contacts/bulk
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/contactBooks/{contactBookId}/contacts/bulk:
    delete:
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
              type: object
              properties:
                contactIds:
                  type: array
                  items:
                    type: string
                  minItems: 1
                  maxItems: 1000
              required:
                - contactIds
      responses:
        '200':
          description: Bulk delete contacts from a contact book
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                  count:
                    type: number
                required:
                  - success
                  - count

````