> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Batch email

Send up to 100 emails in a single request.


## OpenAPI

````yaml post /v1/emails/batch
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/emails/batch:
    post:
      parameters:
        - schema:
            type: string
            minLength: 1
            maxLength: 256
            description: >-
              Pass the optional Idempotency-Key header to make the request safe
              to retry. The key can be up to 256 characters. The server stores
              the canonical request body and behaves as follows:


              - Same key + same request body → returns the original emailId with
              200 OK without re-sending.

              - Same key + different request body → returns 409 Conflict with
              code: NOT_UNIQUE so you can detect the mismatch.

              - Same key while another request is still being processed →
              returns 409 Conflict; retry after a short delay or once the first
              request completes.


              Entries expire after 24 hours. Use a unique key per logical send
              (for example, an order or signup ID).
          required: false
          name: Idempotency-Key
          in: header
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  to:
                    anyOf:
                      - type: string
                      - type: array
                        items:
                          type: string
                  from:
                    type: string
                  subject:
                    type: string
                    minLength: 1
                    description: Optional when templateId is provided
                  templateId:
                    type: string
                    description: ID of a template from the dashboard
                  variables:
                    type: object
                    additionalProperties:
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
                  text:
                    type: string
                    nullable: true
                    minLength: 1
                  html:
                    type: string
                    nullable: true
                    minLength: 1
                  headers:
                    type: object
                    additionalProperties:
                      type: string
                      minLength: 1
                    description: Custom headers to included with the emails
                  attachments:
                    type: array
                    items:
                      type: object
                      properties:
                        filename:
                          type: string
                          minLength: 1
                        content:
                          type: string
                          minLength: 1
                      required:
                        - filename
                        - content
                    maxItems: 10
                  scheduledAt:
                    type: string
                    format: date-time
                  inReplyToId:
                    type: string
                    nullable: true
                required:
                  - to
                  - from
              maxItems: 100
      responses:
        '200':
          description: List of successfully created email IDs
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
                        emailId:
                          type: string
                      required:
                        - emailId
                required:
                  - data

````