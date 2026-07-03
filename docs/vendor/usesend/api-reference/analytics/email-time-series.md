> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Email time series



## OpenAPI

````yaml get /v1/analytics/email-time-series
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/analytics/email-time-series:
    get:
      parameters:
        - schema:
            type: string
            enum:
              - '7'
              - '30'
            description: 'Number of days to retrieve data for (default: 30)'
            example: '30'
          required: false
          name: days
          in: query
        - schema:
            type: string
            description: Filter by domain ID
          required: false
          name: domainId
          in: query
      responses:
        '200':
          description: Retrieve email time series data
          content:
            application/json:
              schema:
                type: object
                properties:
                  result:
                    type: array
                    items:
                      type: object
                      properties:
                        date:
                          type: string
                        sent:
                          type: integer
                        delivered:
                          type: integer
                        opened:
                          type: integer
                        clicked:
                          type: integer
                        bounced:
                          type: integer
                        complained:
                          type: integer
                      required:
                        - date
                        - sent
                        - delivered
                        - opened
                        - clicked
                        - bounced
                        - complained
                  totalCounts:
                    type: object
                    properties:
                      sent:
                        type: integer
                      delivered:
                        type: integer
                      opened:
                        type: integer
                      clicked:
                        type: integer
                      bounced:
                        type: integer
                      complained:
                        type: integer
                    required:
                      - sent
                      - delivered
                      - opened
                      - clicked
                      - bounced
                      - complained
                required:
                  - result
                  - totalCounts

````