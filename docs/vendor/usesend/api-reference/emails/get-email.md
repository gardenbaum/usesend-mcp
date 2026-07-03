> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Get email



## OpenAPI

````yaml get /v1/emails/{emailId}
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/emails/{emailId}:
    get:
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
          description: Retrieve the email
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: string
                  teamId:
                    type: number
                  to:
                    anyOf:
                      - type: string
                      - type: array
                        items:
                          type: string
                  replyTo:
                    anyOf:
                      - type: string
                      - type: array
                        items:
                          type: string
                  cc:
                    anyOf:
                      - type: string
                      - type: array
                        items:
                          type: string
                  bcc:
                    anyOf:
                      - type: string
                      - type: array
                        items:
                          type: string
                  from:
                    type: string
                  subject:
                    type: string
                  html:
                    type: string
                    nullable: true
                  text:
                    type: string
                    nullable: true
                  createdAt:
                    type: string
                  updatedAt:
                    type: string
                  emailEvents:
                    type: array
                    items:
                      type: object
                      properties:
                        emailId:
                          type: string
                        status:
                          type: string
                          enum:
                            - SCHEDULED
                            - QUEUED
                            - SENT
                            - DELIVERY_DELAYED
                            - BOUNCED
                            - REJECTED
                            - RENDERING_FAILURE
                            - DELIVERED
                            - OPENED
                            - CLICKED
                            - COMPLAINED
                            - FAILED
                            - CANCELLED
                            - SUPPRESSED
                        createdAt:
                          type: string
                        data:
                          nullable: true
                      required:
                        - emailId
                        - status
                        - createdAt
                required:
                  - id
                  - teamId
                  - to
                  - from
                  - subject
                  - html
                  - text
                  - createdAt
                  - updatedAt
                  - emailEvents

````