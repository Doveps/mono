FROM python:2
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r savant/requirements.txt
RUN pip install -r bassist/requirements.txt
RUN pip install -e savant/.
RUN pip install -e bassist/.
