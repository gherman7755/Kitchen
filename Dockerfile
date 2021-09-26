FROM python

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirments.txt

EXPOSE 8080

ENV TZ Europe/Moscow

CMD ["python", "main.py"]