> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Reputation metrics



## OpenAPI

````yaml get /v1/analytics/reputation-metrics
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/analytics/reputation-metrics:
    get:
      parameters:
        - schema:
            type: string
            description: Filter by domain ID
          required: false
          name: domainId
          in: query
      responses:
        '200':
          description: Retrieve reputation metrics data
          content:
            application/json:
              schema:
                type: object
                properties:
                  delivered:
                    type: integer
                  hardBounced:
                    type: integer
                  complained:
                    type: integer
                  bounceRate:
                    type: number
                  complaintRate:
                    type: number
                required:
                  - delivered
                  - hardBounced
                  - complained
                  - bounceRate
                  - complaintRate

````