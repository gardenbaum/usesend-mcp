> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Get contact



## OpenAPI

````yaml get /v1/contactBooks/{contactBookId}/contacts/{contactId}
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/contactBooks/{contactBookId}/contacts/{contactId}:
    get:
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
          description: Retrieve the contact
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: string
                  firstName:
                    type: string
                    nullable: true
                  lastName:
                    type: string
                    nullable: true
                  email:
                    type: string
                  subscribed:
                    type: boolean
                    default: true
                  properties:
                    type: object
                    additionalProperties:
                      type: string
                  contactBookId:
                    type: string
                  createdAt:
                    type: string
                  updatedAt:
                    type: string
                required:
                  - id
                  - email
                  - properties
                  - contactBookId
                  - createdAt
                  - updatedAt

````