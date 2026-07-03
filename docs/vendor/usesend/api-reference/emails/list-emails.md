> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# List emails



## OpenAPI

````yaml get /v1/emails
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/emails:
    get:
      parameters:
        - schema:
            type: string
            default: '1'
            example: '1'
          required: false
          name: page
          in: query
        - schema:
            type: string
            default: '50'
            example: '50'
          required: false
          name: limit
          in: query
        - schema:
            type: string
            format: date-time
            example: '2024-01-01T00:00:00Z'
          required: false
          name: startDate
          in: query
        - schema:
            type: string
            format: date-time
            example: '2024-01-31T23:59:59Z'
          required: false
          name: endDate
          in: query
        - schema:
            anyOf:
              - type: string
              - type: array
                items:
                  type: string
            example: '123'
          required: false
          name: domainId
          in: query
      responses:
        '200':
          description: Retrieve a list of emails
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: string
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
                            - nullable: true
                        cc:
                          anyOf:
                            - type: string
                            - type: array
                              items:
                                type: string
                            - nullable: true
                        bcc:
                          anyOf:
                            - type: string
                            - type: array
                              items:
                                type: string
                            - nullable: true
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
                        latestStatus:
                          type: string
                          nullable: true
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
                        scheduledAt:
                          type: string
                          nullable: true
                          format: date-time
                        domainId:
                          type: number
                          nullable: true
                      required:
                        - id
                        - to
                        - from
                        - subject
                        - html
                        - text
                        - createdAt
                        - updatedAt
                        - latestStatus
                        - scheduledAt
                        - domainId
                  count:
                    type: number
                required:
                  - data
                  - count

````