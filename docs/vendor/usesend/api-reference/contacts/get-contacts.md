> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Get contacts



## OpenAPI

````yaml get /v1/contactBooks/{contactBookId}/contacts
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/contactBooks/{contactBookId}/contacts:
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
          required: false
          name: emails
          in: query
        - schema:
            type: number
          required: false
          name: page
          in: query
        - schema:
            type: number
          required: false
          name: limit
          in: query
        - schema:
            type: string
          required: false
          name: ids
          in: query
      responses:
        '200':
          description: Retrieve multiple contacts
          content:
            application/json:
              schema:
                type: array
                items:
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