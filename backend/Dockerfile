# ベースイメージ
FROM python:3.12.0-alpine AS base

WORKDIR /code

# 依存関係のインストール
COPY ./requirements.txt /code/requirements.txt
RUN apk update && \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 開発環境
FROM base AS development
CMD ["python3", "app/main.py"]

# 本番環境
FROM base AS production
COPY ./app /code/app
CMD ["python3", "app/main.py"]

# デフォルトは本番環境を使用
FROM production