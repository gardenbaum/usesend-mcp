> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Pause campaign



## OpenAPI

````yaml post /v1/campaigns/{campaignId}/pause
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/campaigns/{campaignId}/pause:
    post:
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
          description: Pause a campaign
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