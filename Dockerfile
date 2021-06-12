FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

ARG WORKDIR=/dataflow/template
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

# Due to a change in the Beam base image in version 2.24, we need to install
# libffi-dev manually as a dependency. For more information:
#   https://github.com/GoogleCloudPlatform/python-docs-samples/issues/4891
RUN apt-get update && apt-get install -y libffi-dev git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY bigquery_to_pubsub.py .

ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="${WORKDIR}/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/bigquery_to_pubsub.py"

RUN pip install apache-beam[gcp]==2.28.0
RUN pip install -U -r ./requirements.txt