FROM python:3.5-alpine

RUN apk add -U \
	ca-certificates \
 && rm -rf /var/cache/apk/* \
 && pip install --no-cache-dir --upgrade \
	pip \
	setuptools


ADD requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --use-wheel --no-index --find-links=wheeldir \
    -r requirements.txt
ADD run_devpi.py /usr/bin/

ENTRYPOINT ["python3", "/usr/bin/run_devpi.py"]
