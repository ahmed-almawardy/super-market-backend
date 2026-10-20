FROM python:3.13

WORKDIR app

COPY . .
RUN pip install uv && \
    uv export --format requirements-txt -o requirements.txt && \
    pip install -r requirements.txt && \
    rm requirements.txt

EXPOSE 8000