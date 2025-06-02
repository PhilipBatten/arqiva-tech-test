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

# Terraform
- I have split the terraform for the ecr into its own module so it can be provisioned first
- The image can then be pushed to the registry
- The rest of the infra can then be provisioned
    - This will result in a uri being output
```
make deploy // runs the following 3 commands

make provision-ecr
make deploy-image
make provision-infra

make destroy-infra
```

# Improvements
- If I had more time I would have used redis, or other simplier KV store, instead of dynamodb. Dynamodb is simpler to setup quickly due to it being fully managed.
- I would add a github workflow for the deployments. Merging to main would trigger a update of the lambda
- I need to add a command to trigger a lambda update, currently the method is to tear the infra down and run deploy-infra again, or run lambda update manually after pushing the new image
- Unit and integration tests should be added, they were omitted due to the simple nature of the application and the limited set of requirements
- A HTML templating library could be used to better handle rendering, however this seems overkill to start with.
- IAM permissions are very broad, they should be reduced to only what is required.

# Architectural decisions
- Using lambda to run the application is quick to setup and scales quickly, however their can be some latency with cold starts. EC2, ECS or Fargate could also be used to run the docker image.
- Alternatively python could be run directly in lambda using the python runtime, however because I wanted docker locally for testing it seems reasonable to run the same image in both places.
- I split the lambda handler out into its own module, as I did with the local entrypoint. If a change in deployment to a different architecture is needed application code would not need to change.
- The repository module encapsulates the dynamodb implementation, switching this out to a different datastore would be trivial.
- I used terraform as it allows IaC to be located in the same repository. Splitting out the ecr module allowed for a seemless provisioning process. With more time more modules could be split out, however for such a small application this is not needed.
