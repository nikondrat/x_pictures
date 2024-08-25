FROM python:3.11

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y libsm6 libxext6 libxrender-dev gcc git nano mc gettext ffmpeg && \
    apt-get clean

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/project"
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
WORKDIR /usr/src/project
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements/requirements.txt
