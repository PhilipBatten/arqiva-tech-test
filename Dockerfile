FROM public.ecr.aws/lambda/python:3.13 AS lambda

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir -r requirements.txt

COPY src/lambda_function.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda_function.lambda_handler" ]

FROM python:3.13-slim AS local

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/lambda_function.py .
COPY src/app.py .

CMD [ "python", "app.py" ]