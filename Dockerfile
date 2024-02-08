FROM python:latest

# Setup App
ADD . /app

RUN python -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH

CMD ["python","main.py"]