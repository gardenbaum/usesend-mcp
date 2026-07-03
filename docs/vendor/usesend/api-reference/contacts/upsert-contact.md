> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Upsert contact



## OpenAPI

````yaml put /v1/contactBooks/{contactBookId}/contacts/{contactId}
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/contactBooks/{contactBookId}/contacts/{contactId}:
    put:
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
      responses:
        '200':
          description: Contact upserted successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  contactId:
                    type: string
                required:
                  - contactId

````