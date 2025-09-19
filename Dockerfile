# Stage 2: Lambda final image
FROM public.ecr.aws/lambda/python:3.11

# Copy dependencies to /opt/python (Lambda automatically adds this to PYTHONPATH)
COPY --from=builder /app/python /opt/python

# Copy application code
COPY app.py ${LAMBDA_TASK_ROOT}

# Lambda handler
CMD ["app.lambda_handler"]
