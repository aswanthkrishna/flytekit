FROM python:3.11-slim-bookworm

WORKDIR /root
ENV PYTHONPATH /root

COPY . .

# flytekit will autoload the agent if package is installed.
RUN pip install -e .

RUN pip install "prometheus_client"

RUN pip install "skypilot-nightly[aws]"
CMD pyflyte serve agent --port 8000