# Stage 1: Build dependencies
FROM python:3.11-slim AS builder
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target ./python

# Stage 2: Lambda final image
FROM public.ecr.aws/lambda/python:3.11

# Copy dependencies
COPY --from=builder /app/python ${LAMBDA_TASK_ROOT}/python

# Copy application code
COPY app.py ${LAMBDA_TASK_ROOT}

# Lambda handler
CMD ["app.lambda_handler"]