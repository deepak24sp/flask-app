# Stage 1: Build dependencies
FROM python:3.11-slim AS builder
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target ./python

# Stage 2: Lambda final image
FROM public.ecr.aws/lambda/python:3.11

# Copy dependencies from builder stage
COPY --from=builder /app/python ${LAMBDA_TASK_ROOT}/

# Copy application code
COPY app.py ${LAMBDA_TASK_ROOT}

# Set Lambda handler
CMD ["app.lambda_handler"]