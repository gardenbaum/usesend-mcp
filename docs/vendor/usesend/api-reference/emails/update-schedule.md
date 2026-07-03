> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Update schedule



## OpenAPI

````yaml patch /v1/emails/{emailId}
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/emails/{emailId}:
    patch:
      parameters:
        - schema:
            type: string
            minLength: 3
            example: cuiwqdj74rygf74
          required: true
          name: emailId
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
                  format: date-time
              required:
                - scheduledAt
      responses:
        '200':
          description: Retrieve the user
          content:
            application/json:
              schema:
                type: object
                properties:
                  emailId:
                    type: string

````