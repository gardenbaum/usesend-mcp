> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Create domain



## OpenAPI

````yaml post /v1/domains
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/domains:
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
                region:
                  type: string
              required:
                - name
                - region
      responses:
        '200':
          description: Create a new domain
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: number
                    description: The ID of the domain
                    example: 1
                  name:
                    type: string
                    description: The name of the domain
                    example: example.com
                  teamId:
                    type: number
                    description: The ID of the team
                    example: 1
                  status:
                    type: string
                    enum:
                      - NOT_STARTED
                      - PENDING
                      - SUCCESS
                      - FAILED
                      - TEMPORARY_FAILURE
                  region:
                    type: string
                    default: us-east-1
                  clickTracking:
                    type: boolean
                    default: false
                  openTracking:
                    type: boolean
                    default: false
                  publicKey:
                    type: string
                  dkimStatus:
                    type: string
                    nullable: true
                  spfDetails:
                    type: string
                    nullable: true
                  createdAt:
                    type: string
                  updatedAt:
                    type: string
                  dmarcAdded:
                    type: boolean
                    default: false
                  isVerifying:
                    type: boolean
                    default: false
                  errorMessage:
                    type: string
                    nullable: true
                  subdomain:
                    type: string
                    nullable: true
                  verificationError:
                    type: string
                    nullable: true
                  lastCheckedTime:
                    type: string
                    nullable: true
                  dnsRecords:
                    type: array
                    items:
                      type: object
                      properties:
                        type:
                          type: string
                          enum:
                            - MX
                            - TXT
                          description: DNS record type
                          example: TXT
                        name:
                          type: string
                          description: DNS record name
                          example: mail
                        value:
                          type: string
                          description: DNS record value
                          example: v=spf1 include:amazonses.com ~all
                        ttl:
                          type: string
                          description: DNS record TTL
                          example: Auto
                        priority:
                          type: string
                          nullable: true
                          description: DNS record priority
                          example: '10'
                        status:
                          type: string
                          enum:
                            - NOT_STARTED
                            - PENDING
                            - SUCCESS
                            - FAILED
                            - TEMPORARY_FAILURE
                        recommended:
                          type: boolean
                          description: Whether the record is recommended
                      required:
                        - type
                        - name
                        - value
                        - ttl
                        - status
                required:
                  - id
                  - name
                  - teamId
                  - status
                  - publicKey
                  - createdAt
                  - updatedAt
                  - dnsRecords

````