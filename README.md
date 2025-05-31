# Arqiva - Technical Challenge #2 - Backend Software Developer

```
Technical Challenge #2

=================

On a cloud platform of your choice provision a service, using Infrastructure as Code, that serves a html page.

(Feel free to use a cloud provider, language and IaC tooling of your choice, however you should be aware that the primary technologies used at Arqiva are AWS, Python and Terraform respectively)

The content of the page must be ..

<h1>The saved string is dynamic string</h1>

.. Where "dynamic string" can be set to whatever is requested without having to re-deploy. When you demonstrate the solution in the interview you will need to modify the string to show it works. Any user accessing the url must get the same result. You will be asked to take us through the source code.

Accompany this work with a short document (PDF) explaining:

Your solution and discussing the available options

The reasons behind the decisions you made

How you would embellish the solution were you to have more time.

Use the document to explore some of the architectural factors you may face when designing and building a cloud based solution. Also, the pros and cons of the design decisions you needed to make - and, if you had more time, how you would adapt your solution.
```

# Thought process before starting
- An endpoint is needed to serve some html
    - Dynamic value pulled from a data store
        - DynamoDB
        - Redis
        - RDS
- An mechanism to update a value is required
    - Direct DB access?
    - Environment Variable?
    - Endpoint is easiest to use
- First set up a local environment that has the technologies I select
- Second add the endpoints to get the html and set the dynamic value
- Third setup IaC to deploy the solution

# Technology choices
- Python flask to enable multiple endpoints in a single deployment
- AWS Lambda to run the application code
- AWS Api Gateway to give the lambda a public url
- AWS MemoryDB for storing the dynamic value
- Docker for local development
- AWS ECR for docker image storage

# Local development setup
- docker-compose 
    - localstack for dynamodb
    - app
- Dockerfile
    - multi stage
        - local stage for running flask normally
        - lambda stage for running in AWS
- basic application setup that achieves the requirements
    - serve h1 tag with dynamic value
    - set dynamic value via a put in postman/curl

```
# make run // starts the app container and valkey
```

# Changes
- While writing the terraform I realised to use memorydb it would require a vpc, so to simplify the setup I switched to using dynamodb