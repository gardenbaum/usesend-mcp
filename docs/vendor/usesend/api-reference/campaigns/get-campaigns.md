> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Get campaigns



## OpenAPI

````yaml get /v1/campaigns
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/campaigns:
    get:
      parameters:
        - schema:
            type: string
            description: 'Page number for pagination (default: 1)'
            example: '1'
          required: false
          name: page
          in: query
        - schema:
            type: string
            enum:
              - DRAFT
              - SCHEDULED
              - RUNNING
              - PAUSED
              - SENT
            description: Filter campaigns by status
            example: DRAFT
          required: false
          name: status
          in: query
        - schema:
            type: string
            description: Search campaigns by name or subject
            example: newsletter
          required: false
          name: search
          in: query
      responses:
        '200':
          description: Get list of campaigns
          content:
            application/json:
              schema:
                type: object
                properties:
                  campaigns:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: string
                        name:
                          type: string
                        from:
                          type: string
                        subject:
                          type: string
                        createdAt:
                          type: string
                          format: date-time
                        updatedAt:
                          type: string
                          format: date-time
                        status:
                          type: string
                        scheduledAt:
                          type: string
                          nullable: true
                          format: date-time
                        total:
                          type: integer
                        sent:
                          type: integer
                        delivered:
                          type: integer
                        unsubscribed:
                          type: integer
                      required:
                        - id
                        - name
                        - from
                        - subject
                        - createdAt
                        - updatedAt
                        - status
                        - scheduledAt
                        - total
                        - sent
                        - delivered
                        - unsubscribed
                  totalPage:
                    type: integer
                required:
                  - campaigns
                  - totalPage

````