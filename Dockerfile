FROM python:3.10-slim

WORKDIR /workspace

RUN pip install redis

CMD ["bash"]