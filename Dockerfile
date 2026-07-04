FROM ubuntu:latest
LABEL authors="embraass"

FROM python:3.14

WORKDIR /app

# Сначала копируем requirements.txt в контейнер
COPY . .

# Теперь устанавливаем зависимости из скопированного файла
RUN pip install --upgrade pip && \
    pip install -r requirements.txt



ENTRYPOINT ["top", "-b"]