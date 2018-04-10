FROM python:3.6-onbuild

ADD private.py /
# ADD main.py /

CMD ["python", "./main.py"]
