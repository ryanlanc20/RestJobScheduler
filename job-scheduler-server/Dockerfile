FROM python:3.10
COPY ./ ./
WORKDIR /
RUN pip3 install pipenv
RUN pipenv install
CMD ["pipenv","run","python3","scheduler.py"]
EXPOSE 5000