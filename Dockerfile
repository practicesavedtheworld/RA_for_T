FROM python:3.11

RUN mkdir /ra_app

WORKDIR /ra_app

COPY requirements.txt .
COPY dev-requirements.txt .
COPY app_dep.sh .
COPY mode_changer.py .

RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install -r dev-requirements.txt

COPY . .
RUN chmod a+x /ra_app/*.sh

