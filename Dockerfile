FROM python:3
COPY requirements.txt /requirements.txt
RUN pip install pip==18.1  # pygit failed to install in latest pip version
RUN pip install -r /requirements.txt
COPY src /src
COPY main.py /main.py
CMD ["python", "/main.py"]
