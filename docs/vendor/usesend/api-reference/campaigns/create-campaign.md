> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Create campaign



## OpenAPI

````yaml post /v1/campaigns
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/campaigns:
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                  minLength: 1
                from:
                  type: string
                  minLength: 1
                subject:
                  type: string
                  minLength: 1
                previewText:
                  type: string
                contactBookId:
                  type: string
                  minLength: 1
                content:
                  type: string
                  minLength: 1
                html:
                  type: string
                  minLength: 1
                replyTo:
                  anyOf:
                    - type: string
                      minLength: 1
                    - type: array
                      items:
                        type: string
                        minLength: 1
                cc:
                  anyOf:
                    - type: string
                      minLength: 1
                    - type: array
                      items:
                        type: string
                        minLength: 1
                bcc:
                  anyOf:
                    - type: string
                      minLength: 1
                    - type: array
                      items:
                        type: string
                        minLength: 1
                sendNow:
                  type: boolean
                scheduledAt:
                  type: string
                  description: >-
                    Timestamp in ISO 8601 format or natural language (e.g.,
                    'tomorrow 9am', 'next monday 10:30')
                batchSize:
                  type: integer
                  minimum: 1
                  maximum: 100000
              required:
                - name
                - from
                - subject
                - contactBookId
      responses:
        '200':
          description: Create a campaign
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