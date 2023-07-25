# syntax=docker/dockerfile:1
# Author § Victor-ray, S.
FROM sanicframework/sanic:LTS
COPY ./server.py ./requirements.txt /srv/
RUN pip install --upgrade pip; pip install -r /srv/requirements.txt
EXPOSE 8080
CMD ["python", "/srv/server.py"]
