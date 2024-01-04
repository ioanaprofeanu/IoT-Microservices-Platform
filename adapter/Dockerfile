FROM python:3.10

# # set work directory
WORKDIR /adapter

# # copy and install dependencies
COPY requirements.txt /adapter/
RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy api files
COPY . /adapter/

# command for running the server
CMD ["python", "-u", "adapter.py"]