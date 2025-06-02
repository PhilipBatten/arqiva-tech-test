FROM public.ecr.aws/lambda/python:3.13 AS lambda

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir -r requirements.txt

COPY src/app.py ${LAMBDA_TASK_ROOT}
COPY src/repository.py ${LAMBDA_TASK_ROOT}

COPY src/lambda.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda.lambda_handler" ]

FROM python:3.13-slim AS local

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/app.py .
COPY src/repository.py .

COPY src/local.py .
COPY src/lambda.py .
COPY setup_localstack.py .

CMD [ "python", "local.py" ]