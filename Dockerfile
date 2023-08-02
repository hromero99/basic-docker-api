FROM python:3.11-bullseye
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT ["bash","/app/entrypoint.sh"]