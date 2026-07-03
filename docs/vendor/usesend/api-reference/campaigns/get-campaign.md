> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Get campaign



## OpenAPI

````yaml get /v1/campaigns/{campaignId}
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/campaigns/{campaignId}:
    get:
      parameters:
        - schema:
            type: string
            minLength: 1
            example: cmp_123
          required: true
          name: campaignId
          in: path
      responses:
        '200':
          description: Get campaign details
          content:
            application/json:
              schema:
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
                  previewText:
                    type: string
                    nullable: true
                  contactBookId:
                    type: string
                    nullable: true
                  html:
                    type: string
                    nullable: true
                  content:
                    type: string
                    nullable: true
                  status:
                    type: string
                  scheduledAt:
                    type: string
                    nullable: true
                    format: date-time
                  batchSize:
                    type: integer
                  batchWindowMinutes:
                    type: integer
                  total:
                    type: integer
                  sent:
                    type: integer
                  delivered:
                    type: integer
                  opened:
                    type: integer
                  clicked:
                    type: integer
                  unsubscribed:
                    type: integer
                  bounced:
                    type: integer
                  hardBounced:
                    type: integer
                  complained:
                    type: integer
                  replyTo:
                    type: array
                    items:
                      type: string
                  cc:
                    type: array
                    items:
                      type: string
                  bcc:
                    type: array
                    items:
                      type: string
                  createdAt:
                    type: string
                    format: date-time
                  updatedAt:
                    type: string
                    format: date-time
                required:
                  - id
                  - name
                  - from
                  - subject
                  - previewText
                  - contactBookId
                  - html
                  - content
                  - status
                  - scheduledAt
                  - batchSize
                  - batchWindowMinutes
                  - total
                  - sent
                  - delivered
                  - opened
                  - clicked
                  - unsubscribed
                  - bounced
                  - hardBounced
                  - complained
                  - replyTo
                  - cc
                  - bcc
                  - createdAt
                  - updatedAt

````