FROM ubuntu:16.04
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install --upgrade pip
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r savant/requirements.txt
RUN pip install -r bassist/requirements.txt
RUN pip install -e savant/.
RUN pip install -e bassist/.
ENTRYPOINT ["python"]
CMD ["savant/run.py"]
