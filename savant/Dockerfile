# Dockerfile
# NOTE: depends on context being in parent directory
# Example to build from parent directory:
# docker build -t savant -f savant/Dockerfile .
FROM python:2
RUN mkdir /mono
COPY savant /mono/savant
COPY bassist /mono/bassist
WORKDIR /mono/savant
RUN pip install -r requirements.txt
RUN pip install -r /mono/bassist/requirements.txt
RUN pip install -e .
RUN pip install -e /mono/bassist/.
ENTRYPOINT ["python"]
CMD ["run.py"]
