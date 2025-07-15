FROM alpine:latest
RUN apk add --no-cache libpq-dev musl-dev gcc python3-dev py3-pip
WORKDIR /app
COPY requirements.txt .
RUN python3 -m venv venv
RUN . venv/bin/activate
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
