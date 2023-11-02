FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# TO DO: check if I'm obscuring and doing this correctly
ENV DATABASE_URL=DATABASE_URL

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
