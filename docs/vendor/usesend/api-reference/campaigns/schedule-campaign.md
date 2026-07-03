> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Schedule campaign



## OpenAPI

````yaml post /v1/campaigns/{campaignId}/schedule
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/campaigns/{campaignId}/schedule:
    post:
      parameters:
        - schema:
            type: string
            minLength: 1
            example: cmp_123
          required: true
          name: campaignId
          in: path
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                scheduledAt:
                  type: string
                  description: >-
                    Timestamp in ISO 8601 format or natural language (e.g.,
                    'tomorrow 9am', 'next monday 10:30')
                batchSize:
                  type: integer
                  minimum: 1
                  maximum: 100000
      responses:
        '200':
          description: Schedule a campaign
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                required:
                  - success

````