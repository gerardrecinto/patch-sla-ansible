# Reproducible runner for the playbooks and tests. Works with docker, podman, and buildah bud.
FROM python:3.12-slim
RUN pip install --no-cache-dir ansible-core==2.20.* pytest
WORKDIR /work
COPY . .
RUN ansible-galaxy collection install -r ansible/requirements.yml
CMD ["python", "-m", "pytest", "-q", "tests"]
