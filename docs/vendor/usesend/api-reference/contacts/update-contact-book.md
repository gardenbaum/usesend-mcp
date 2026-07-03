> ## Documentation Index
> Fetch the complete documentation index at: https://docs.usesend.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Update contact book



## OpenAPI

````yaml patch /v1/contactBooks/{contactBookId}
openapi: 3.0.0
info:
  version: 1.0.0
  title: useSend API
servers:
  - url: https://app.usesend.com/api
security: []
paths:
  /v1/contactBooks/{contactBookId}:
    patch:
      parameters:
        - schema:
            type: string
            example: clx1234567890
          required: true
          name: contactBookId
          in: path
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
                emoji:
                  type: string
                properties:
                  type: object
                  additionalProperties:
                    type: string
                doubleOptInEnabled:
                  type: boolean
                doubleOptInFrom:
                  type: string
                  nullable: true
                doubleOptInSubject:
                  type: string
                doubleOptInContent:
                  type: string
                variables:
                  type: array
                  items:
                    type: string
      responses:
        '200':
          description: Update the contact book
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: string
                    description: The ID of the contact book
                    example: clx1234567890
                  name:
                    type: string
                    description: The name of the contact book
                    example: Newsletter Subscribers
                  teamId:
                    type: number
                    description: The ID of the team
                    example: 1
                  properties:
                    type: object
                    additionalProperties:
                      type: string
                    description: Custom properties for the contact book
                    example:
                      customField1: value1
                  variables:
                    type: array
                    items:
                      type: string
                    description: >-
                      Allowed personalization variables for contacts in this
                      book
                    example:
                      - registrationCode
                      - company
                  emoji:
                    type: string
                    description: The emoji associated with the contact book
                    example: 📙
                  doubleOptInEnabled:
                    type: boolean
                    description: Whether double opt-in is enabled for new contacts
                    example: true
                  doubleOptInFrom:
                    type: string
                    nullable: true
                    description: >-
                      From address used for double opt-in emails (must use a
                      verified domain)
                    example: Newsletter <hello@example.com>
                  doubleOptInSubject:
                    type: string
                    nullable: true
                    description: Subject line used for double opt-in confirmation email
                    example: Please confirm your subscription
                  doubleOptInContent:
                    type: string
                    nullable: true
                    description: >-
                      Email editor JSON content used for double opt-in
                      confirmation
                  createdAt:
                    type: string
                    description: The creation timestamp
                  updatedAt:
                    type: string
                    description: The last update timestamp
                  _count:
                    type: object
                    properties:
                      contacts:
                        type: number
                        description: The number of contacts in the contact book
                    required:
                      - contacts
                required:
                  - id
                  - name
                  - teamId
                  - properties
                  - variables
                  - emoji
                  - createdAt
                  - updatedAt
        '403':
          description: Forbidden - API key doesn't have access to this contact book
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                required:
                  - error
        '404':
          description: Contact book not found
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                required:
                  - error

````